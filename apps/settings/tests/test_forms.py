from django.contrib.auth.hashers import make_password
from django.test import TestCase

from apps.settings.forms import ChangePasswordForm, CronForm, ProfileForm
from apps.web.models import Profile


class FormTestCase(TestCase):
    """Test forms"""

    def setUp(self):
        self.user = Profile.objects.create(
            username="tester",
            password=make_password("asdf"),
            email="tester1@dubell.io",
            timezone="UTC",
            notifications_enabled=False,
        )

    def test_profile_form(self):
        """Test profile forms should succeed"""
        data = {"timezone": "UTC", "notifications_enabled": True}
        form = ProfileForm(data=data, user=self.user)

        self.assertTrue(form.is_valid())

    def test_profile_form_fail(self):
        """Test profile forms should fail"""
        data = {"timezone": "DoesNot/Exist", "notifications_enabled": "True"}
        form = ProfileForm(data=data, user=self.user)

        self.assertFalse(form.is_valid())

    def test_updating_crontab(self):
        """Test updating crontab entry should succeed"""

        form = CronForm(data={"cron": "13 13 * * *"}, user=self.user)
        self.assertTrue(form.is_valid())

    def test_updating_crontab_invalid(self):
        """Test updating invalid crontab entries should fail"""

        form = CronForm(data={"cron": "* * * * *"}, user=self.user)
        self.assertFalse(form.is_valid())

        form = CronForm(data={"cron": "345 12 * * *"}, user=self.user)
        self.assertFalse(form.is_valid())

    def test_change_passwords(self):
        """Test chaning password form, should succeed"""

        data = {
            "old_password": "asdf",
            "new_password1": "1234",
            "new_password2": "1234",
        }
        form = ChangePasswordForm(data=data, user=self.user)

        self.assertTrue(form.is_valid())

    def test_change_passwords_invalid(self):
        """Test chaning password form, should succeed"""

        data = {"old_password": "", "new_password1": "1234", "new_password2": "1234"}
        form = ChangePasswordForm(data=data, user=self.user)

        self.assertFalse(form.is_valid())

        data = {
            "old_password": "asdf",
            "new_password1": "ERROR",
            "new_password2": "1234",
        }
        form = ChangePasswordForm(data=data, user=self.user)

        self.assertFalse(form.is_valid())

        data = {
            "old_password": "asdf",
            "new_password1": "1234",
            "new_password2": "ERROR",
        }
        form = ChangePasswordForm(data=data, user=self.user)

        self.assertFalse(form.is_valid())
