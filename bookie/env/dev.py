""" Development profile for running Bookie in dev mode """

from bookie.settings import *

DEBUG = True
DJANGO_LOG_LEVEL = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0@#t#6sv7c)975k16xmb#6$=##7#e3=$#=b7lbo51e^ku^!7*p'

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

if not TELEGRAM_API_KEY:
    print("TELEGRAM_API_KEY not set, setting value to 123:123. Change this if you want to test telegram integration.")
    TELEGRAM_API_KEY = "123:123"


ALLOWED_HOSTS = ["*"]
