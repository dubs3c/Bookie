""" tests """

from datetime import timedelta
import json
from unittest import mock

from django.contrib.auth.hashers import make_password
from django.test import Client, TestCase
from django.urls import reverse

from apps.settings.models import Telegram
from apps.web.models import Bookmarks, Profile


class TelegramApiTestCase(TestCase):
    """
    Test the telegram web hook that Telegram
    backend services uses to send messages to Bookie
    """

    def setUp(self):
        """ Initialize variables """
        self.client = Client()
        self.telegram_api = reverse("api:index")
        self.telegram_request = {
            "message": {
                "chat": {
                    "first_name": "Bookie", "last_name": "Man", "id": 958276750,
                    "type": "private", "username": "dabookieman"
                },
                "date": 1553084337,
                "from": {
                    "first_name": "Bookie", "id": 975378798,
                    "is_bot": False, "language_code": "en",
                    "username": "dabookieman"
                },
                "message_id": 190,
                "photo": list([
                    {
                        "file_id": "afhaugafagageg", "file_size": 1432,
                        "height": 90, "width": 67
                    },
                    {
                        "file_id": "figjopsrjgklnvsouhrog", "file_size": 16149,
                        "height": 320, "width": 240
                    },
                    {
                        "file_id": "fjfoishrgouggea", "file_size": 73321,
                        "height": 800, "width": 601
                    },
                    {
                        "file_id": "fkskafjgishgousofgsg", "file_size": 120691,
                        "height": 1280, "width": 962
                    }
                ]),
                "text": "hello",
                "update_id": 8563829
            }
        }

        self.user = Profile.objects.create(
            username="tester", password=make_password("asdf"),
            email="tester1@dubell.io", timezone="UTC"
        )

    @mock.patch("requests.Session.post")
    def test_register_telegram_account(self, mock_requests):
        """ Test registrating a telegram account """
        mock_requests.return_value.status_code = 200

        obj = Telegram.objects.create(user=self.user, telegram_username="dabookieman", token="1234")

        self.telegram_request["message"]["text"] = f"/register {obj.token}"
        data = json.dumps(self.telegram_request)

        with mock.patch('utils.telegram.send_message') as mock_send:
            mock_send.return_value = (True, "Success")
            response = self.client.post(self.telegram_api, data, content_type="application/json")

            self.assertEqual(response.status_code, 201)
            self.assertTrue(Telegram.objects.get(user=self.user).activated)

    @mock.patch("requests.Session.post")
    @mock.patch('apps.api.views.send_message')
    def test_register_telegram_account_no_token(self, mock_send, mock_requests):
        """ Telegram account registration without sending a token """
        mock_requests.return_value.status_code = 200
        mock_send.return_value = (True, "Success")

        Telegram.objects.create(user=self.user, telegram_username="dabookieman", token="1234")

        self.telegram_request["message"]["text"] = "/register "
        data = json.dumps(self.telegram_request)
        response = self.client.post(self.telegram_api, data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_with(self.telegram_request["message"]["chat"]["id"], "You forgot to enter your code...")

    @mock.patch("requests.Session.post")
    @mock.patch('apps.api.views.send_message')
    def test_register_telegram_too_many_arguments(self, mock_send, mock_requests):
        """ User sent too many arguments to Bookie via their telegram account """
        mock_requests.return_value.status_code = 200
        mock_send.return_value = (True, "Success")

        Telegram.objects.create(user=self.user, telegram_username="dabookieman", token="1234")

        self.telegram_request["message"]["text"] = "/register 1234 1234"
        data = json.dumps(self.telegram_request)
        response = self.client.post(self.telegram_api, data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_with(self.telegram_request["message"]["chat"]["id"],
                                     "Please register with this format: /register token, where token is your token "
                                     "from Bookie")

    @mock.patch("requests.Session.post")
    @mock.patch('apps.api.views.send_message')
    def test_register_telegram_account_token_already_activated(self, mock_send, mock_requests):
        """ User has already activated their telegram account with the specific token """
        mock_requests.return_value.status_code = 200
        mock_send.return_value = (True, "Success")

        obj = Telegram.objects.create(user=self.user, telegram_username="dabookieman", token="1234", activated=True)

        self.telegram_request["message"]["text"] = f"/register {obj.token}"
        data = json.dumps(self.telegram_request)
        response = self.client.post(self.telegram_api, data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_with(self.telegram_request["message"]["chat"]["id"],
                                     "Bookie has already activated your account with this token!")

    @mock.patch("requests.Session.post")
    @mock.patch('apps.api.views.send_message')
    def test_register_telegram_success(self, mock_send, mock_requests):
        """ User successfully activated their telegram account """
        mock_requests.return_value.status_code = 200
        mock_send.return_value = (True, "Success")

        obj = Telegram.objects.create(user=self.user, telegram_username="dabookieman", token="1234")

        self.telegram_request["message"]["text"] = f"/register {obj.token}"
        data = json.dumps(self.telegram_request)
        response = self.client.post(self.telegram_api, data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        mock_send.assert_called_with(self.telegram_request["message"]["chat"]["id"],
                                     "Success, your telegram account is now linked to Bookie!")

    @mock.patch("requests.Session.post")
    @mock.patch("apps.api.views.send_message")
    def test_register_telegram_token_expired(self, mock_send, mock_requests):
        """ User's token has expired """
        mock_requests.return_value.status_code = 200
        mock_send.return_value = (True, "Success")

        obj = Telegram.objects.create(user=self.user, telegram_username="dabookieman", token="1234")

        with mock.patch("apps.api.views.timezone.now") as mock_date:
            mock_date.return_value = obj.created + timedelta(minutes=10)

            self.telegram_request["message"]["text"] = f"/register {obj.token}"
            data = json.dumps(self.telegram_request)
            response = self.client.post(self.telegram_api, data, content_type="application/json")

            self.assertEqual(response.status_code, 200)
            mock_send.assert_called_with(self.telegram_request["message"]["chat"]["id"],
                                         "Your token has expired, a new one has been generted.")

    @mock.patch("apps.api.views.parse_article")
    @mock.patch("requests.Session.post")
    @mock.patch('apps.api.views.send_message')
    def test_add_bookmarks(self, mock_send, mock_requests, mock_parse_article):
        """ User successfully creates a bookmark """
        mock_requests.return_value.status_code = 200
        mock_send.return_value = (True, "Success")
        mock_parse_article.return_value = {"description": "A super cool website",
                                           "title": "Probably the best website in the world",
                                           "image": "",
                                           "body": ""}

        Telegram.objects.create(user=self.user, telegram_username="dabookieman",
                                token="1234", activated=True)

        self.telegram_request["message"]["text"] = "https://dubell.io"
        data = json.dumps(self.telegram_request)
        response = self.client.post(self.telegram_api, data, content_type="application/json")
        bkm = Bookmarks.objects.get(user=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(bkm.description, "A super cool website")

    @mock.patch("requests.Session.post")
    @mock.patch("apps.api.views.send_message")
    def test_username_does_not_exist(self, mock_send, mock_requests):
        """ Username does not exist """
        mock_requests.return_value.status_code = 200
        mock_send.return_value = (True, "Success")

        Telegram.objects.create(user=self.user, telegram_username="dabookieman", token="1234")

        self.telegram_request["message"]["from"]["username"] = "Wrong username"
        data = json.dumps(self.telegram_request)
        response = self.client.post(self.telegram_api, data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_with(self.telegram_request["message"]["chat"]["id"],
                                     "That Telegram account name does not exist in Bookie, \
                                   have you entered your username/firstname/lastname correctly?")
