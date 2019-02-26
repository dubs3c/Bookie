""" Telegram integration utilities """

import requests

from django.conf import settings

BASE_URL = "https://api.telegram.org"
TOKEN = settings.TELEGRAM_API_KEY
API = f"{BASE_URL}/bot{TOKEN}"
SESSION = requests.Session()

def send_message(chat_id: str, message: str):
    """ Send message to user """
    data = {"chat_id": chat_id, "text": message}
    resp = SESSION.post(f"{API}/sendMessage", data=data)
    if resp.status_code >= 200 and resp.status_code < 300:
        return (True, "Success")
    else:
        return (False, resp.status_code)
