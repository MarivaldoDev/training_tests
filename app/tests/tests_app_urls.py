from django.test import TestCase
from django.urls import reverse


class AppURLsTests(TestCase):
    def test_app_home_url_is_correct(self):
        url = reverse("app:home")
        self.assertEqual(url, "/")

    def test_app_tasks_by_category_url_is_correct(self):
        url = reverse("app:tasks_by_category", kwargs={"category_id": 1})
        self.assertEqual(url, "/tasks/category/1/")

    def test_app_category_url_is_correct(self):
        url = reverse("app:categories")
        self.assertEqual(url, "/categories/")

    def test_app_tasks_url_is_correct(self):
        url = reverse("app:tasks")
        self.assertEqual(url, "/tasks/")

    def test_app_task_detail_url_is_correct(self):
        url = reverse("app:task_detail", kwargs={"task_id": 1})
        self.assertEqual(url, "/tasks/details/1/")

    def test_app_toggle_task_completed_url_is_correct(self):
        url = reverse("app:toggle_task_completed", kwargs={"task_id": 1})
        self.assertEqual(url, "/tasks/details/1/toggle/")
