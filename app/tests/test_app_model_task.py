from .test_base_app import AppTestBase


class AppTaskModelTests(AppTestBase):
    def setUp(self):
        self.task = self.make_task(title="Work")
        return super().setUp()

    def test_app_model_task_str_method(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.title} ({self.task.category.name}) - {'Completed' if self.task.completed else 'Not Completed'}",
        )
