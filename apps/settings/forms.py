""" forms """

import json
import re
import pytz

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django_celery_beat.models import PeriodicTasks

from apps.web.models import CrontabScheduleUser, ScheduledTasks
from apps.web.models import Profile


class ChangePasswordForm(forms.Form):
    """User password change form"""

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your old password"}
        ),
        required=False,
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your new password"}
        ),
        required=False,
    )

    new_password2 = forms.CharField(
        label=_("Verify new password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Verify your new password"}
        ),
        required=False,
    )

    error_messages = {
        "password_mismatch": (
            "The new password did not match the verification password."
        ),
        "both_pass_fields": (
            "If you are changing your password, you need to enter all fields."
        ),
        "password_incorrect": _(
            "Your old password was entered incorrectly. Please enter it again."
        ),
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """Validates that the old_password field is correct."""
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages["password_incorrect"], code="password_incorrect"
            )
        return old_password

    def clean_new_password2(self):
        """Validate that the new passwords match"""
        oldpw = self.cleaned_data.get("old_password")
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch"
            )
        return password2

    def save(self, commit=True):
        """Save the new password for the user"""
        if self.cleaned_data.get("new_password2"):
            self.user.set_password(self.cleaned_data.get("new_password2"))
            if commit:
                self.user.save()
        return self.user


class ProfileForm(ModelForm):
    """Profile form"""

    error_messages = {
        "incorrect_timezone": ("The timezone you selected is incorrect."),
        "incorrect_notification_type": (
            "Notification enabled should be true or false."
        ),
    }

    class Meta:
        model = Profile
        fields = ["timezone", "notifications_enabled"]
        widgets = {
            "timezone": forms.Select(attrs={"class": "custom-select custom-select-sm"})
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_timezone(self):
        """Validate timezone"""
        timezone = self.cleaned_data.get("timezone")
        if timezone not in pytz.all_timezones:
            raise forms.ValidationError(
                self.error_messages["incorrect_timezone"], code="incorrect_timezone"
            )
        return timezone

    def clean_notifications_enabled(self):
        """Validate notifications_enabled"""
        enabled = self.cleaned_data.get("notifications_enabled")
        if type(enabled) is not bool:
            raise forms.ValidationError(
                self.error_messages["incorrect_notification_type"],
                code="incorrect_notification_type",
            )
        return enabled

    def save(self, commit=True):
        """save"""
        enabled = self.cleaned_data.get("notifications_enabled")
        timezone = self.cleaned_data.get("timezone")

        ScheduledTasks.objects.filter(user=self.user).update(enabled=enabled)
        CrontabScheduleUser.objects.filter(user=self.user).update(timezone=timezone)

        Profile.objects.filter(user=self.user).update(
            notifications_enabled=enabled, timezone=timezone
        )

        return enabled


class CronForm(forms.Form):
    """Construct the form for cron expressions"""

    cron = forms.CharField(max_length=13, label="Cron", widget=forms.HiddenInput())

    error_messages = {
        "incorrect_length": ("The cron expression is to damn long!"),
        "incorrect_pattern": ("The cron expression is wrong"),
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_cron(self):
        """Validate the cron expression"""

        cron = self.cleaned_data.get("cron")
        # TODO - Improve regex to make sure cron expression is correct
        regex = re.compile(
            "[0-9]{1,2}\s[0-9]{1,2}\s(?:[0-9]{1,2}|[*])\s(?:[0-9]{1,2}|[*])\s(?:[0-9]{1,2}|[*])"
        )

        if len(cron.split(" ")) > 5:
            raise forms.ValidationError(
                self.error_messages["incorrect_length"], code="incorrect_length"
            )

        if re.match(regex, cron) is None:
            raise forms.ValidationError(
                self.error_messages["incorrect_pattern"], code="incorrect_pattern"
            )

        return cron

    def save(self, commit=True):
        """Save the new password for the user"""
        cron = self.cleaned_data.get("cron")
        if cron:
            cron_list = cron.split(" ")

            updated = CrontabScheduleUser.objects.filter(user=self.user).update(
                minute=cron_list[0],
                hour=cron_list[1],
                day_of_week=cron_list[2],
                day_of_month=cron_list[3],
                month_of_year=cron_list[4],
                timezone=pytz.timezone(self.user.profile.timezone),
                user=self.user,
            )

            if updated == 0 or not updated:
                user_crontab = CrontabScheduleUser.objects.create(
                    minute=cron_list[0],
                    hour=cron_list[1],
                    day_of_week=cron_list[2],
                    day_of_month=cron_list[3],
                    month_of_year=cron_list[4],
                    timezone=pytz.timezone(self.user.profile.timezone),
                    user=self.user,
                )

                if self.user.profile.notifications_enabled:
                    ScheduledTasks.objects.create(
                        crontab=user_crontab,
                        args=json.dumps([self.user.pk]),
                        name=f"Notify {self.user.email}",
                        task="notify",
                        user=self.user.profile,
                    )
            else:
                # fuck too lazy - fix later
                user_crontab = CrontabScheduleUser.objects.get(user=self.user)
                if self.user.profile.notifications_enabled:
                    try:
                        obj = ScheduledTasks.objects.get(user=self.user)
                    except ObjectDoesNotExist:
                        obj = ScheduledTasks.objects.create(
                            crontab=user_crontab,
                            args=json.dumps([self.user.pk]),
                            name=f"Notify {self.user.email}",
                            task="notify",
                            user=self.user.profile,
                        )

                    PeriodicTasks.changed(obj)

        return cron
