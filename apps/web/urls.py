from django.urls import path

from . import views

app_name = "web"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("delete_bookmark", views.delete_bookmark, name="delete_bookmark"),
    path("mark_bookmark", views.mark_read, name="mark_bookmark_read"),
    path("add_bookmark", views.add_bookmark, name="add_bookmark"),
    path("bookmark/<str:bookmark_id>", views.view_bookmark, name="view_bookmark"),
    path(
        "bookmark/tag/<str:bookmark_id>",
        views.add_bookmark_tag,
        name="add_bookmark_tag",
    ),
    path("iframe/<str:bookmark_id>", views.bookmark_iframe, name="bookmark_iframe"),
]
