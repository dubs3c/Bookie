"""
Contains all the dashboard views
"""

import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .forms import RegistrationForm
from .models import Bookmarks


LOGGER = logging.getLogger(__name__)

def index(request):
    """ Dashboard page """
    query_param = request.GET.get("filter")
    if query_param:
        if query_param == "notread":
            bookmarks = Bookmarks.objects.filter(user=request.user, read=False).order_by("-created")
        if query_param == "read":
            bookmarks = Bookmarks.objects.filter(user=request.user, read=True).order_by("-created")
    else:
        bookmarks = Bookmarks.objects.filter(user=request.user).order_by("-created")

    context = {"bookmarks": bookmarks}
    return render(request, "web/index.html", context)


def settings(request):
    """ Settings page """
    return render(request, "web/settings.html")


def delete_bookmark(request):
    """ Feletes a bookmark """
    if request.method == "POST":
        data = request.POST
        user = request.user
        bookmark_id = data["bm_id"]

        bookmark = get_object_or_404(Bookmarks, bm_id=bookmark_id)

        if bookmark.user == user:
            bookmark.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse("bow chicka bow wow", content_type="text/plain")

def mark_read(request):
    """ Mark a bookmark as read """
    if request.method == "POST":
        data = request.POST
        user = request.user
        bookmark_id = data["bm_id"]

        bookmark = get_object_or_404(Bookmarks, bm_id=bookmark_id)

        if bookmark.user == user:
            if bookmark.read:
                bookmark.read = False
            else:
                bookmark.read = True
            bookmark.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse("Introducing, neals...", content_type="text/plain")


def user_login(request):
    """ Login user """

    if request.user.is_authenticated:
        return redirect(reverse("web:index"))

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("web:index"))
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
        return redirect(reverse("web:index"))

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
