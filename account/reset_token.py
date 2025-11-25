import jwt
from datetime import timedelta, datetime
from django.conf import settings

def create_password_reset_token(user):
    payload =  {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "type": "password_reset"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def verify_password_reset_token(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if decoded.get("type") != "password_reset":
            return None, None
        return decoded.get("user_id"), decoded.get("email")
    except Exception:
        return None, None