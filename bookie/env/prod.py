""" Production profile for running Bookie in prod mode """

from bookie.settings import *

DJANGO_SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_DOMAINS = os.environ["ALLOWED_DOMAINS"].split(",")

DEBUG = False
DJANGO_LOG_LEVEL = DEBUG

ALLOWED_HOSTS = [ALLOWED_DOMAINS]
INTERNAL_IPS = ['127.0.0.1']
