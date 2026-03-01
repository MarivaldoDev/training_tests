from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Category, Task


class TasksTestBase(TestCase):
    def setUp(self):
        return super().setUp()

    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_user(self, username="user", password="123456"):
        return User.objects.create(username=username, password=password)

    def make_task(
        self,
        title="Task 1",
        description="Description for Task 1",
        category_data=None,
        author_data=None,
        start_date="2026-01-01",
        completed=False,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Task.objects.create(
            title=title,
            description=description,
            category=self.make_category(**category_data),
            author=self.make_user(**author_data),
            start_date=start_date,
            completed=completed,
        )
