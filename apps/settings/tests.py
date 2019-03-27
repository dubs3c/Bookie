""" tests """

from datetime import timedelta
import json
from unittest import mock

from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.web.models import Profile
from apps.settings.views import integration_telegram, integration_telegram_delete

from .models import Telegram

class TelegramIntegrationTestCase(TestCase):
    """ Test the Telegram API integration """

    def setUp(self):
        """ Setup DB """
        self.factory = RequestFactory()
        self.user = Profile.objects.create(username="Tester", password="asdf", email="tester1@dubell.io")

    def test_create_telegram_integration(self):
        """ Test creating a Telegram integration """
        view = integration_telegram
        url = reverse("settings:telegram_integration")
        
        data = {"telegram_username": "thetester"}

        request = self.factory.post(url, data, format="json")
        request.user = self.user
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Telegram.objects.count(), 1)
        self.assertEqual(Telegram.objects.get(id=1).telegram_username, data["telegram_username"])

    def test_create_telegram_integration_exists(self):
        """ User already has a Telegram integration """
        view = integration_telegram
        url = reverse("settings:telegram_integration")

        Telegram.objects.create(user=self.user, telegram_username="tester", token="12345", activated=True)
        self.assertEqual(Telegram.objects.count(), 1)

        data = {"telegram_username": "tester"}

        request = self.factory.post(url, data)
        request.user = self.user
        response = view(request)

        token = json.loads(response.content.decode()).get("token")

        self.assertEqual(token, Telegram.objects.get(user=self.user).token)
        self.assertEqual(Telegram.objects.get(id=1).telegram_username, data["telegram_username"])

    def test_create_telegram_integration_exists_new_token(self):
        """ User already has a Telegram integration but the token has expired """
        view = integration_telegram
        url = reverse("settings:telegram_integration")

        obj = Telegram.objects.create(user=self.user, telegram_username="tester", token="12345", activated=True)
        
        with mock.patch('django.utils.timezone.now') as mock_date:
            mock_date.return_value = obj.created + timedelta(minutes=10)

            data = {"telegram_username": "tester"}

            request = self.factory.post(url, data)
            request.user = self.user
            response = view(request)

            token = json.loads(response.content.decode()).get("token")

            self.assertEqual(token, Telegram.objects.get(user=self.user).token)
            self.assertNotEqual(Telegram.objects.get(user=self.user).token, "12345")
            self.assertEqual(Telegram.objects.get(id=1).telegram_username, data["telegram_username"])

    def test_delete_telegram_integration(self):
        """ Test deleting a Telegram integration """
        view = integration_telegram_delete
        url = reverse("settings:integration_telegram_delete")

        Telegram.objects.create(user=self.user, telegram_username="tester", token="12345", activated=True)
        
        self.assertEqual(Telegram.objects.count(), 1)
        
        request = self.factory.post(url)
        request.user = self.user
        response = view(request)

        self.assertEqual(Telegram.objects.count(), 0)
        self.assertEqual(response.status_code, 302)


class SettingsTestCase():
    """ Test settings functionality """
    
    def setUp():
        pass

    def test_change_password(self):
        """ Test updating password """
        pass

    def test_change_pasword_fail(self):
        """ Test faling of password validation """
        pass

    def test_enable_notifications(self):
        """ Test enabling email notification """
        pass

    def test_updating_timezone(self):
        """ Test updating user's timezone """
        pass

    def test_delete_account(self):
        """ Test deleting the user account """
        pass

    def test_updating_crontab(self):
        """ Test updating crontab entry """
        pass
    
    def test_updating_crontab_invalid(self):
        """ Test updating invalid crontab entries """
        pass