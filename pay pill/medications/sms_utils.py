import os
import requests


def normalize_sa_phone(raw_phone):
    """
    Normalize a South African phone number to E.164 for TextBee.
    '0821234567' -> '+27821234567'; already-E.164 numbers are left as-is.
    Shared by every call site that sends a real SMS, so the same normalization
    logic isn't duplicated and can't drift between them.
    """
    phone = str(raw_phone).strip()
    if phone.startswith('0'):
        phone = '+27' + phone[1:]
    elif not phone.startswith('+'):
        phone = '+27' + phone
    return phone


def send_sms_via_textbee(phone_number, message_text):
    """Send an SMS via TextBee using the device-specific endpoint."""
    api_key = os.environ.get('TEXTBEE_API_KEY')
    device_id = os.environ.get('TEXTBEE_DEVICE_ID')

    if not api_key or not device_id:
        return {"error": "TextBee credentials not set"}

    url = f"https://api.textbee.dev/api/v1/gateway/devices/{device_id}/send-sms"

    payload = {
        "recipients": [phone_number],
        "message": message_text
    }

    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
