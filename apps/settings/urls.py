""" URLs """

from django.urls import path

from . import views

app_name = "settings"
urlpatterns = [
    path("", views.settings, name="index"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("change_password", views.change_password, name="change_password"),
    path("integrations", views.integrations, name="integrations"),
    path("portability", views.data_portability, name="data_portability"),
    path("integrations/<str:integration>", views.integration_detail, name="integration_detail"),
    path("telegram", views.integration_telegram, name="telegram_integration"),
    path("telegram/delete", views.integration_telegram_delete, name="integration_telegram_delete")
]