""" Test web Utils """

from unittest import mock

from django.test import SimpleTestCase

from utils.web import https_upgrade, is_url, is_url_blacklisted


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
        self.assertEqual(https_upgrade(domain), domain)
        self.assertEqual(https_upgrade(www), www)
        self.assertEqual(https_upgrade(test1), https)
        self.assertEqual(https_upgrade(test2), test2)


    def test_is_url_blacklisted(self):
        """ A request will always include protocol.
        :return:
        """
        self.assertTrue(is_url_blacklisted("http://LocAlHosT"))
        self.assertTrue(is_url_blacklisted("http://localhost/"))
        self.assertTrue(is_url_blacklisted("http://localhost:80/"))
        self.assertTrue(is_url_blacklisted("http://127.0.0.1"))
        self.assertTrue(is_url_blacklisted("hTTPs://169.254.169.254"))
        self.assertTrue(is_url_blacklisted("hTTPs://localhost:80"))

        self.assertFalse(is_url_blacklisted("http://www.localhost.com"))
        self.assertFalse(is_url_blacklisted("http://localhost.co.uk"))


    def test_is_url(self):
        test_cases = (
            (is_url("https://dubell.io"), True),
            (is_url("http://dubell.io"), True),
            (is_url("https://bookie.dubell.io"), True),
            (is_url("https://dubell.io/some/path/"), True),
            (is_url("dubell.io"), False),
            (is_url("ftp://some-server.local"), False),
            (is_url("1.1.1.1"), False),
            (is_url("http://0xA9FEA9FE/"), False),
            (is_url("http://user:password@dubell.io"), False),
            (is_url("http://user@dubell.io"), False),
        )

        for test_case in test_cases:
            self.assertEqual(test_case[0], test_case[1])