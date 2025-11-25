from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.conf import settings
signer = TimestampSigner()

def generate_verification_token(user):
    value = f"{user.pk}:{user.email}"
    return signer.sign(value)

def verify_token(token, max_age=60*60*24):
    try:
        unsigned = signer.unsign(token, max_age=max_age)
        user_id, email = unsigned.split(":")
        return int(user_id), email
    except (BadSignature,SignatureExpired):
        return None, None

def send_verification_email(user):
    token = generate_verification_token(user)
    url = f"{settings.FRONTED_URL}/verify-email/{token}"

    subject = "Email verification"
    message = f"Hello {user.username}, click the link below to complete verification"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )