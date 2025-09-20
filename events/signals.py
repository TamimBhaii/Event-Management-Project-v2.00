from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP

@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        event = instance.event
        subject = f"RSVP Confirmation for {event.title}"
        message = f"Hi {user.get_full_name() or user.username},\n\nYou have successfully RSVP'd as '{instance.status}' to the event: {event.title}."
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        except Exception:
            pass

        try:
            send_mail(f"New RSVP for {event.title}", f"{user} RSVPed as {instance.status}", settings.DEFAULT_FROM_EMAIL, [event.organizer.email])
        except Exception:
            pass
