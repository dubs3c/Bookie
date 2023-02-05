"""
Contains all the setting views
"""

from datetime import timedelta
import logging
import pytz
import csv

from django.http import Http404, HttpResponseBadRequest
from django.utils.crypto import get_random_string
from django.template.exceptions import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect

from apps.web.models import CrontabScheduleUser, Bookmarks
from .forms import ChangePasswordForm, CronForm, ProfileForm, SiteSettingsForm
from .models import Telegram, Site


LOGGER = logging.getLogger(__name__)


def settings(request):
    """Settings index page"""
    try:
        cron_obj = CrontabScheduleUser.objects.get(user=request.user)
        cron_expression = f"{cron_obj.minute} {cron_obj.hour} {cron_obj.day_of_week} \
            {cron_obj.day_of_month} {cron_obj.month_of_year}"
    except ObjectDoesNotExist:
        cron_expression = ""

    timezones = pytz.all_timezones
    change_pw_form = ChangePasswordForm(user=request.user)
    errors = []

    if request.method == "GET":
        profile_form = ProfileForm(
            user=request.user.profile, instance=request.user.profile
        )
        cron_form = CronForm(user=request.user.profile)

    if request.method == "POST":
        profile_form = ProfileForm(data=request.POST, user=request.user.profile)
        cron_form = CronForm(data=request.POST, user=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been successfully updated")
        else:
            errors.append(profile_form.errors)

        if cron_form.is_valid():
            cron_form.save()
        else:
            errors.append(cron_form.errors)

    return render(
        request,
        "settings/account.html",
        context={
            "change_pw_form": change_pw_form,
            "profile_form": profile_form,
            "cron_form": cron_form,
            "timezones": timezones,
            "cron_expression": cron_expression,
            "formerrors": errors,
        },
    )


def change_password(request):
    """Change user password endpoint"""
    errors = []
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been successfully updated")
        else:
            errors.append(form.errors)

    return render(request, "settings/account.html", context={"formerrors": errors})


def integrations(request):
    """integrations page"""
    user = request.user
    telegram = Telegram.objects.filter(user=user)
    if telegram:
        data = {"telegram": telegram[0].activated}
    else:
        data = {}
    return render(request, "settings/integrations.html", context=data)


def data_portability(request):
    """Export bookmarks"""

    if request.method == "POST":
        user = request.user
        bookmarks = (
            Bookmarks.objects.filter(user=user)
            .values(
                "bm_id",
                "title",
                "link",
                "image",
                "description",
                "read",
                "created",
                "tags__name",
                "body",
            )
            .order_by("-id")
        )

        merged = {}
        if bookmarks:
            # The bookmarks object will contain duplicates because of the many2many field on tags.
            # Items needs to be merged.
            for item in bookmarks:
                if not item["bm_id"] in merged.keys():
                    merged[item["bm_id"]] = item
                else:
                    tags = item["tags__name"]
                    x = merged[item["bm_id"]]
                    if tags and x["tags__name"]:
                        x["tags__name"] += f", {tags}"
                        merged[item["bm_id"]] = x

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="bookie_output.csv"'
        writer = csv.writer(response, delimiter=";")
        writer.writerow(
            ["Title", "Link", "Image", "Description", "Read", "Created", "Tags", "Body"]
        )
        for key, bm in merged.items():
            writer.writerow(
                [
                    bm.get("title"),
                    bm.get("link"),
                    bm.get("image"),
                    bm.get("description"),
                    bm.get("read"),
                    bm.get("created"),
                    bm.get("tags__name"),
                    bm.get("body"),
                ]
            )
        return response
    return render(request, "settings/dataportability.html")


def integration_detail(request, integration):
    """Render the specific integration page"""
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
    """telegram integration"""

    if request.method == "POST":
        user = request.user
        telegram_username = request.POST.get("telegram_username")
        if not telegram_username:
            return HttpResponse(status=404)
        telegram = Telegram.objects.filter(user=user)
        if telegram.count() == 1:
            obj = telegram[0]
            if timezone.now() < (obj.created + timedelta(minutes=3)):
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
    """Delete the telegram integration"""
    user = request.user
    if request.method == "POST":
        telegram = Telegram.objects.filter(user=user)
        if telegram.exists():
            telegram.delete()

    return redirect(reverse("settings:integrations"))


def delete_account(request):
    """Delete your account"""
    if request.method == "POST":
        user = request.user
        User.objects.filter(pk=user.pk).delete()
        messages.success(request, "Your account was successfully deleted")
        return redirect(reverse("login"))

    return redirect(reverse("settings:index"))


def users(request):
    if not request.user.is_superuser:
        raise Http404()

    users = User.objects.raw(
        """
            SELECT u.id, u.username, count(b.id) as bookmarks, u.is_active, u.is_superuser, u.last_login
            FROM auth_user as u
            LEFT JOIN web_bookmarks as b
            ON b.user_id = u.id
            GROUP BY u.id
            ORDER BY u.id;
        """
    )
    return render(request, "settings/users.html", context={"users": users})


def delete_user(request, user_id):
    if not request.user.is_superuser:
        raise Http404()
    if request.method == "POST":
        # todo: change this lol
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return HttpResponse(status=200)
    else:
        raise Http404()


def deactivate_user(request, user_id):
    if not request.user.is_superuser:
        raise Http404()
    if request.method == "POST":
        # todo: change this lol
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
        return HttpResponse(status=200)
    else:
        raise Http404()


def site(request):
    if not request.user.is_superuser:
        raise Http404()

    errors = []

    if request.method == "GET":
        s = Site.objects.all().first()
        data = {"allow_registration": s.allow_registration}
        site_form = SiteSettingsForm(data)

    if request.method == "POST":
        site_form = SiteSettingsForm(data=request.POST)

        if site_form.is_valid():
            site_form.save()
            messages.success(request, "Site settings has been successfully updated")
        else:
            errors.append(site_form.errors)

    return render(request, "settings/site.html", context={ "form": site_form, "formerrors": errors})
