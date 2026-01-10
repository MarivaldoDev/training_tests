from django.test import TestCase
from django.urls import resolve, reverse

from app import views


class AppViewsTests(TestCase):
    def test_app_home_view_function_is_correct(self):
        view = resolve(reverse("app:home"))
        self.assertIs(view.func, views.home)
