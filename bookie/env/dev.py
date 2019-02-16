""" Development profile for running Bookie in dev mode """

from bookie.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0@#t#6sv7c)975k16xmb#6$=##7#e3=$#=b7lbo51e^ku^!7*p'

DEBUG = True
DJANGO_LOG_LEVEL = DEBUG

ALLOWED_HOSTS = ["*"]
