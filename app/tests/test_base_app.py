from django.test import TestCase

from ..models import Category, Task


class AppTestBase(TestCase):
    def setUp(self):
        return super().setUp()

    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_task(
        self,
        title="Task 1",
        description="Description for Task 1",
        category_data=None,
        start_date="2026-01-01",
        completed=False,
    ):
        if category_data is None:
            category_data = {}

        return Task.objects.create(
            title=title,
            description=description,
            category=self.make_category(**category_data),
            start_date=start_date,
            completed=completed,
        )
