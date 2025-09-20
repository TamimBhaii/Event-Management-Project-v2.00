from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings


def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
    )

    #  Subject
    subject = "Activate your EventManager account"

    #  Render HTML email template
    html_message = render_to_string("email/account_activation_email.html", {
        "user": user,
        "activation_link": activation_link,
    })

    #  Plain text fallback (if email client doesn't support HTML)
    plain_message = strip_tags(html_message)

    #  Send mail
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
