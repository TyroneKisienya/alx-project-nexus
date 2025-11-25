from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .reset_token import create_password_reset_token, verify_password_reset_token

def send_password_reset_email(user):
    token = create_password_reset_token(user)
    reset_url = f"{settings.FRONTEND_URL}/ password-reset?token={token}"

    subject = "Reset Password"
    message = f"Click to reset password:\n\n{reset_url}\n\nThe link expires in 30 minutes"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['user.email'],
        fail_silently=False
    )
    return True

def validate_password_reset_token(token):
    return verify_password_reset_token(token)