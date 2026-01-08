from django.test import TestCase
from django.urls import reverse


class AppURLsTests(TestCase):
    def test_app_home_url_is_correct(self):
        url = reverse("app:home")
        self.assertEqual(url, "/")

