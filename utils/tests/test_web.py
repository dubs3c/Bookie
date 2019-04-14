""" Test web Utils """

from unittest import mock

from django.test import SimpleTestCase

from utils.web import https_upgrade


class WebUtilsTestCase(SimpleTestCase):
    """ Tests """

    @mock.patch("utils.web.requests.get")
    def test_https_upgrade(self, mock_requests):
        """ Test """
        mock_requests.return_value.status_code = 200

        http = "http://dubell.io"
        https = "https://dubell.io"
        domain = "dubell.io"
        www = "www.dubell.io"
        test1 = "HtTP://dubell.io"
        test2 = "HtTPs://dubell.io"

        self.assertEqual(https_upgrade(http), https)
        self.assertEqual(https_upgrade(https), https)
        self.assertEqual(https_upgrade(domain), https)
        self.assertEqual(https_upgrade(www), f"https://{www}")
        self.assertEqual(https_upgrade(test1), https)
        self.assertEqual(https_upgrade(test2), test2)
