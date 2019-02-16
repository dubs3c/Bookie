""" URLs for API endpoints """

from django.urls import path

from bookie.settings import TELEGRAM_API_KEY

from . import views

TELEGRAM_KEY = TELEGRAM_API_KEY.split(":")[1]

app_name = "api"
urlpatterns = [
    path(f'telegram/{TELEGRAM_KEY}/', views.telegram_api, name='index')
]