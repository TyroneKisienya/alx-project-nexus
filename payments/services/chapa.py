import uuid
import requests
from django.conf import settings

def initialize_payment(amount, email, first_name, last_name, callback_url):
    tx_ref = str(uuid.uuid4())

    payload = {
        "amount": str(amount),
        "currency": "KES",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "tx_ref": tx_ref,
        "callback_url": callback_url,
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{settings.CHAPA_BASE_URL}/transaction/initialize",
        json=payload,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()
    return response.json(), tx_ref
