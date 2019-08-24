"""
Contains all the dashboard views
"""

import logging

from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import RegistrationForm
from .models import Bookmarks, BookmarkTags
from utils.web import is_url, parse_article


LOGGER = logging.getLogger(__name__)

def index(request):
    """ index page """
    if request.user.is_authenticated:
        return redirect(reverse("web:dashboard"))

    return redirect(reverse("login"))


def dashboard(request):
    """ Dashboard page """
    query_param = request.GET.get("filter")
    page_id = request.GET.get("page")
    if query_param:
        if query_param == "unread":
            bookmarks = Bookmarks.objects.filter(user=request.user, read=False).order_by("-created")
        if query_param == "read":
            bookmarks = Bookmarks.objects.filter(user=request.user, read=True).order_by("-created")
    else:
        bookmarks = Bookmarks.objects.filter(user=request.user).order_by("-created")

    paginator = Paginator(bookmarks, 10)
    if page_id:
        page = paginator.get_page(page_id)
    else:
        page = paginator.get_page(1)
    context = {"bookmarks": page}
    return render(request, "web/index.html", context)


def view_bookmark(request, bookmark_id):
    """ View a specific bookmark """
    bookmark = get_object_or_404(Bookmarks, user=request.user, bm_id=bookmark_id)
    return render(request, "web/bookmark.html", {"bookmark": bookmark, 'body_class': "bookmark-detail"})


def bookmark_iframe(request, bookmark_id):
    """ View article body in a sandboxed iframe """
    bookmark = get_object_or_404(Bookmarks, user=request.user, bm_id=bookmark_id)
    return render(request, "web/bookmark_sandbox.html", {"bookmark": bookmark})

def add_bookmark_tag(request, bookmark_id):
    """ Add a tag for a given bookmark """
    if request.method == "POST":
        bookmark = get_object_or_404(Bookmarks, user=request.user, bm_id=bookmark_id)
        tag = request.POST.get("tag")
        bookmark_tag, bookmark_tag_created = BookmarkTags.objects.get_or_create(name=tag)
        bookmark.tags.add(bookmark_tag)
        return HttpResponse(status=201)

    if request.method == "DELETE":
        req = QueryDict(request.body)
        tag = req.get("tag")
        bookmark = get_object_or_404(Bookmarks, user=request.user, bm_id=bookmark_id)
        bookmark_tag = get_object_or_404(BookmarkTags, name=tag, bookmarks__user=request.user, bookmarks__bm_id=bookmark_id)
        bookmark.tags.remove(bookmark_tag)
        return HttpResponse(status=200)

    return HttpResponse(status=405)

def settings(request):
    """ Settings page """
    return render(request, "web/settings.html")


def add_bookmark(request):
    """ Add a link from the dashboard """
    if request.method == "POST":
        req_data = request.POST
        data = req_data.get("data")
        if is_url(data):
            parsed_html = parse_article(data)
            Bookmarks.objects.create(user=request.user, link=data,
                                     description=parsed_html["description"],
                                     title=parsed_html["title"],
                                     image=parsed_html["image"],
                                     body=parsed_html["body"])
            return HttpResponse(status=200)
        else:
            Bookmarks.objects.create(user=request.user, link=data)
            return HttpResponse(status=200)

    return HttpResponse(status=405)


def delete_bookmark(request):
    """ Feletes a bookmark """
    if request.method == "POST":
        data = request.POST
        user = request.user
        bookmark_id = data.get("bm_id")

        bookmark = get_object_or_404(Bookmarks, bm_id=bookmark_id, user=user)

        bookmark.delete()
        return HttpResponse(status=200)

    return HttpResponse("bow chicka bow wow", content_type="text/plain")

def mark_read(request):
    """ Mark a bookmark as read """
    if request.method == "POST":
        data = request.POST
        user = request.user
        bookmark_id = data.get("bm_id")

        bookmark = get_object_or_404(Bookmarks, bm_id=bookmark_id, user=user)

        if bookmark.read:
            bookmark.read = False
        else:
            bookmark.read = True

        bookmark.save()
        return HttpResponse(status=200)


    return HttpResponse("Introducing, neals...", content_type="text/plain")


def user_login(request):
    """ Login user """

    if request.user.is_authenticated:
        return redirect(reverse("web:dashboard"))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            data = {"error": "Please enter both username and password."}
            return render(request, "registration/login.html", context=data)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("web:dashboard"))
        else:
            data = {"error": "Wrong username/password"}
            return render(request, "registration/login.html", context=data)
    if request.method == "GET":
        return render(request, "registration/login.html")


def user_logout(request):
    """ logout user """
    logout(request)
    return redirect(reverse("login"))

def register(request):
    """ Register a new user """
    if request.user.is_authenticated:
        return redirect(reverse("web:dashboard"))

    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully registered, please login.")
            return redirect(reverse("login"))
        else:
            return render(request, "registration/registration.html", context={"form": form})

    if request.method == "GET":
        form = RegistrationForm()
        return render(request, "registration/registration.html", context={"form": form})
