from django.test import TestCase
from django.urls import resolve, reverse

from app import views


class AppViewsTests(TestCase):
    def test_app_home_view_function_is_correct(self):
        view = resolve(reverse("app:home"))
        self.assertIs(view.func, views.home)

    def test_app_tasks_view_function_is_correct(self):
        view = resolve(reverse("app:tasks"))
        self.assertIs(view.func, views.task_list)

    def test_app_category_view_function_is_correct(self):
        view = resolve(reverse("app:categories"))
        self.assertIs(view.func, views.category_list)

    def test_app_tasks_by_category_view_function_is_correct(self):
        view = resolve(reverse("app:tasks_by_category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.tasks_by_category)

    def test_app_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("app:home"))
        self.assertEqual(response.status_code, 200)

    def test_app_home_view_loads_correct_template(self):
        response = self.client.get(reverse("app:home"))
        self.assertTemplateUsed(response, "home.html")
