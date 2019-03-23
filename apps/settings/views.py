"""
Contains all the setting views
"""

from datetime import timedelta
import json
import logging
import pytz

from django.utils.crypto import get_random_string
from django.template.exceptions import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect

from apps.web.models import CrontabScheduleUser
from .forms import ChangePasswordForm, CronForm, ProfileForm
from .models import Telegram


LOGGER = logging.getLogger(__name__)

def settings(request):
    """ Settings index page """
    timezones = pytz.all_timezones
    cron_obj = CrontabScheduleUser.objects.get(user=request.user)
    cron_expression = f"{cron_obj.minute} {cron_obj.hour} {cron_obj.day_of_week} \
        {cron_obj.day_of_month} {cron_obj.month_of_year}"
    change_pw_form = ChangePasswordForm(user=request.user)
    errors = []

    if request.method == "GET":
        profile_form = ProfileForm(user=request.user.profile, instance=request.user.profile)
        cron_form = CronForm(user=request.user.profile)

    if request.method == "POST":
        profile_form = ProfileForm(data=request.POST, user=request.user.profile)
        cron_form = CronForm(data=request.POST, user=request.user.profile)


        if profile_form.is_valid() and cron_form.is_valid():
            cron_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been successfully updated")
        else:
            errors.append(profile_form.errors)
            errors.append(cron_form.errors)


    return render(request, "settings/account.html",
                  context={"change_pw_form": change_pw_form, "profile_form": profile_form,
                           "cron_form": cron_form, "timezones": timezones,
                           "cron_expression": cron_expression, "formerrors": errors})

def change_password(request):
    """ Change user password endpoint """

    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been successfully updated")

    return redirect(reverse("settings:index"))


def integrations(request):
    """ integrations page """
    user = request.user
    telegram = Telegram.objects.filter(user=user)
    if telegram:
        data = {"telegram": telegram[0].activated}
    else:
        data = {}
    return render(request, "settings/integrations.html", context=data)


def data_portability(request):
    """ Export bookmarks """
    return render(request, "settings/dataportability.html")


def integration_detail(request, integration):
    """ Render the specific integration page """
    if not integration.isalpha():
        return HttpResponse("Can't find what you are looking for...", status=404)
    try:
        template = get_template(f"settings/{integration}.html")
    except TemplateDoesNotExist:
        return HttpResponse("Can't find what you are looking for...", status=404)
    except TemplateSyntaxError:
        LOGGER.error(f"Syntax error in template: {integration}")
        return HttpResponse("This should not have happened", status=404)

    return render(request, template.template.name)


def integration_telegram(request):
    """ telegram integration """

    if request.method == "POST":
        user = request.user
        telegram_username = request.POST["telegram_username"]
        if not telegram_username:
            return HttpResponse(status=404)
        telegram = Telegram.objects.filter(user=user)
        if telegram.count() == 1:
            obj = telegram[0]
            if obj.created < (obj.created + timedelta(minutes=3)):
                token = {"token": obj.token}
                return JsonResponse(token)
            else:
                obj.token = get_random_string(length=5)
                obj.save()
                token = {"token": obj.token}
                return JsonResponse(token, status=200)
        else:
            token = get_random_string(5)
            t = Telegram(user=user, telegram_username=telegram_username, token=token)
            t.save()
            return JsonResponse({"token": token}, status=201)


def integration_telegram_delete(request):
    """ Delete the telegram integration """
    user = request.user
    if request.method == "POST":
        telegram = Telegram.objects.filter(user=user)
        if telegram.exists():
            telegram.delete()

    return redirect(reverse("settings:integrations"))


def delete_account(request):
    """ Delete your account """
    if request.method == "POST":
        user = request.user
        User.objects.filter(pk=user.pk).delete()
        messages.success(request, "Your account was successfully deleted")
        return redirect(reverse("login"))

    return redirect(reverse("settings:index"))
