from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        # mark inactive and send activation
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        activation_link = f"http://localhost:8000/accounts/activate/{uid}/{token}/"
        subject = "Activate your EventManager account"
        message = f"Hi {instance.username},\n\nPlease click the link below to activate your account:\n\n{activation_link}\n\nIf you didn't register, ignore this message."
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])
        except Exception:
            # fail silently in dev
            pass
