from django.urls import resolve, reverse

from app import views

from .test_base_app import AppTestBase


class AppViewsTests(AppTestBase):
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

    def test_app_tasks_template_shows_no_tasks_message_when_no_tasks(self):
        response = self.client.get(reverse("app:tasks"))
        self.assertIn(b"<p>Nenhuma tarefa encontrada.</p>", response.content)

    def test_app_tasks_template_loads_tasks(self):
        self.make_task()
        response = self.client.get(reverse("app:tasks"))
        content = response.content.decode("utf-8")
        response_context_tasks = response.context["tasks"]

        self.assertIn("Task 1", content)
        self.assertEqual(len(response_context_tasks), 1)

    def test_app_tasks_detail_view_function_is_correct(self):
        view = resolve(reverse("app:task_detail", kwargs={"task_id": 1}))
        self.assertIs(view.func, views.task_detail)

    def test_app_toggle_task_completed_view_function_is_correct(self):
        view = resolve(reverse("app:toggle_task_completed", kwargs={"task_id": 1}))
        self.assertIs(view.func, views.toggle_task_completed)
