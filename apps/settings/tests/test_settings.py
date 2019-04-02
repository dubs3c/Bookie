""" tests """

from django.contrib.auth.hashers import check_password, make_password
from django.test import Client, TestCase
from django.urls import reverse

from apps.web.models import CrontabScheduleUser, Profile

class SettingsTestCase(TestCase):
    """ Test settings functionality """

    def setUp(self):
        self.client = Client()
        self.change_password_url = reverse("settings:change_password")
        self.settings_index_url = reverse("settings:index")
        self.user = Profile.objects.create(
            username="tester", password=make_password("asdf"),
            email="tester1@dubell.io", timezone="UTC"
            )

    def test_change_password(self):
        """ Test updating password """
        data = {"old_password": "asdf", "new_password1": "1234", "new_password2": "1234"}

        self.client.force_login(self.user)
        response = self.client.post(self.change_password_url, data, follow=True)

        self.assertEqual(
            check_password("1234", Profile.objects.get(username="tester").password), True
            )

        self.assertContains(response, "Your password has been successfully updated")

    def test_change_pasword_wrong_password_fail(self):
        """ Test faling password validation by entering the wrong old_password """
        data = {"old_password": "wrong", "new_password1": "1234", "new_password2": "1234"}

        self.client.force_login(self.user)
        response = self.client.post(self.change_password_url, data, follow=True)

        self.assertContains(
            response, "Your old password was entered incorrectly. Please enter it again."
            )

        self.assertEqual(
            check_password("asdf", Profile.objects.get(username="tester").password), True
            )

    def test_change_password_mismatch_fail(self):
        """ Test password validation by failing password verification """
        data = {"old_password": "asdf", "new_password1": "1234", "new_password2": "WRONG!!"}

        self.client.force_login(self.user)
        response = self.client.post(self.change_password_url, data, follow=True)

        self.assertContains(response, "The new password did not match the verification password.")
        self.assertEqual(
            check_password("asdf", Profile.objects.get(username="tester").password), True
            )

    def test_update_profile(self):
        """ Update Profile """
        data = {"timezone": "Europe/Stockholm", "cron": "14 14 * * *"}

        self.client.force_login(self.user)
        self.client.post(self.settings_index_url, data, follow=True)

        cron = CrontabScheduleUser.objects.get(user=self.user.profile)
        cron_str = f"{cron.minute} {cron.hour} {cron.day_of_week} {cron.day_of_month} {cron.month_of_year}"

        self.assertEqual(data["cron"], cron_str)
        self.assertEqual(self.user.profile.timezone, data["timezone"])

    def test_update_profile_fail(self):
        """ Test failing updating profile form """
        data = {"timezone": "Stockholm/Europe", "cron": "* 14 * * *"}

        self.client.force_login(self.user)
        response = self.client.post(self.settings_index_url, data, follow=True)

        self.assertContains(response, f"Select a valid choice. {data['timezone']} is not one of the available choices.")
        self.assertNotEqual(self.user.profile.timezone, data["timezone"])
        self.assertFalse(CrontabScheduleUser.objects.filter(user=self.user.profile))

    def test_delete_account(self):
        """ Test deleting the user account """
        self.client.force_login(self.user)
        data = {"timezone": "Europe/Stockholm", "cron": "14 14 * * *"}
        self.client.post(self.settings_index_url, data, follow=True)

        self.client.post(reverse("settings:delete_account"), {}, follow=True)

        self.assertFalse(Profile.objects.filter(user=self.user))
        self.assertFalse(CrontabScheduleUser.objects.filter(user=self.user))
