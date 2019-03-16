""" Production profile for running Bookie in prod mode """

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from bookie.settings import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_DOMAINS = os.environ["ALLOWED_DOMAINS"].split(",")


SENTRY_KEY = os.environ.get("SENTRY_KEY", "")

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_SENDER = os.environ['EMAIL_SENDER']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_SSL = True

DJANGO_POSTGRESQL_HOST = os.environ['DJANGO_POSTGRESQL_HOST']
DJANGO_POSTGRESQL_DBNAME = os.environ['DJANGO_POSTGRESQL_DBNAME']
DJANGO_POSTGRESQL_USER = os.environ['DJANGO_POSTGRESQL_USER']
DJANGO_POSTGRESQL_PASS = os.environ['DJANGO_POSTGRESQL_PASS']

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DJANGO_POSTGRESQL_DBNAME,
        'USER': DJANGO_POSTGRESQL_USER,
        'PASSWORD': DJANGO_POSTGRESQL_PASS,
        'HOST': DJANGO_POSTGRESQL_HOST,
        'PORT': '5432',
        'OPTIONS': {

        },
    }
}