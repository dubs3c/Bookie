from django.urls import path

from . import views

app_name = "web"
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("delete_bookmark", views.delete_bookmark, name="delete_bookmark"),
    path("mark_bookmark", views.mark_read, name="mark_bookmark_read")
]