""" tests """

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from apps.web.models import Profile


class LoginTestCase(TestCase):
    """ Test Login and registration """

    def setUp(self):
        self.user1 = Profile.objects.create(
            username="tester1", password=make_password("asdf"),
            email="tester1@dubell.io", timezone="UTC"
            )
        self.user2 = Profile.objects.create(
            username="tester2", password=make_password("asdf"),
            email="tester2@dubell.io", timezone="UTC"
            )
        self.login_url = reverse("login")
        self.register_url = reverse("register")


    def test_login(self):
        """ Login with correct account credentials """
        data = {"username": self.user1.username, "password": "asdf"}
        response = self.client.post(self.login_url, data, follow=True)

        self.assertRedirects(response, expected_url=reverse("web:dashboard"))

    def test_login_fail(self):
        """ Login in with incorrect account credentials """
        data = {"username": self.user1.username, "password": "WRONG"}
        response = self.client.post(self.login_url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Wrong username/password", response.content.decode())

    def test_registration(self):
        """ Successfully register an account """
        data = {
            "username": "dabookieman",
            "email": "dabookieman@bookie.dubell.io",
            "password1": "asdfasdf123",
            "password2": "asdfasdf123"
            }
        response = self.client.post(self.register_url, data, follow=True)

        self.assertRedirects(response, expected_url=reverse("login"))
        self.assertTrue(Profile.objects.filter(username="dabookieman").exists())

    def test_registration_email_exists(self):
        """ Fail user registration, user already exists """
        data = {
            "username": "dabookieman",
            "email": self.user1.email,
            "password1": "asdfasdf123",
            "password2": "asdfasdf123"
            }
        response = self.client.post(self.register_url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Email address already exists.", response.content.decode())

    def test_access_dashboard_authenticated(self):
        """ Access dashboard while authenticated """
        self.client.force_login(self.user1)
        response = self.client.get(reverse("web:dashboard"), follow=True)

        self.assertEqual(response.status_code, 200)

    def test_access_dashboard_not_authenticated(self):
        """ Access dashboard while not being authenticated """
        response = self.client.get(reverse("web:dashboard"), follow=True)

        self.assertRedirects(response, expected_url=reverse("login"))
