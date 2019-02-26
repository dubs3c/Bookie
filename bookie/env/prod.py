""" Production profile for running Bookie in prod mode """

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from bookie.settings import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_DOMAINS = os.environ["ALLOWED_DOMAINS"].split(",")


SENTRY_KEY = os.environ.get("SENTRY_KEY", "")

DEBUG = False
DJANGO_LOG_LEVEL = DEBUG
STATIC_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ALLOWED_DOMAINS
INTERNAL_IPS = ['127.0.0.1']

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

if not TELEGRAM_API_KEY:
    print("TELEGRAM_API_KEY was not set, exiting...")
    quit()

if SENTRY_KEY:
    sentry_sdk.init(
        dsn=SENTRY_KEY,
        integrations=[DjangoIntegration()]
    )
