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

    def test_app_category_view_loads_categories_where_tasks_exist(self):
        self.make_category(name="Category 1")
        self.make_category(name="Category 2")
        self.make_task(category_data={"name": "Category 1"})

        response = self.client.get(reverse("app:categories"))
        content = response.content.decode("utf-8")
        response_context_categories = response.context["categories"]

        self.assertIn("Category 1", content)
        self.assertNotIn("Category 2", content)
        self.assertEqual(len(response_context_categories), 1)

    def test_app_tasks_by_category_view_function_is_correct(self):
        view = resolve(reverse("app:tasks_by_category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.tasks_by_category)

    def test_app_tasks_by_category_view_category_not_found_returns_404(self):
        category = self.make_category()
        response = self.client.get(
            reverse("app:tasks_by_category", kwargs={"category_id": category.id + 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_app_tasks_by_category_view_loads_tasks(self):
        self.make_task(category_data={"name": "Category 1"})
        response = self.client.get(
            reverse("app:tasks_by_category", kwargs={"category_id": 1})
        )
        content = response.content.decode("utf-8")
        response_context_tasks = response.context["tasks"]

        self.assertIn("Task 1", content)
        self.assertEqual(len(response_context_tasks), 1)

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

    def test_app_tasks_detail_view_task_not_found_returns_404(self):
        task = self.make_task()
        response = self.client.get(
            reverse("app:task_detail", kwargs={"task_id": task.id + 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_app_tasks_detail_view_loads_task(self):
        task = self.make_task()
        response = self.client.get(
            reverse("app:task_detail", kwargs={"task_id": task.id})
        )
        content = response.content.decode("utf-8")
        response_context_task = response.context["task"]

        self.assertIn("Task 1", content)
        self.assertEqual(response_context_task, task)

    def test_app_toggle_task_completed_view_function_is_correct(self):
        view = resolve(reverse("app:toggle_task_completed", kwargs={"task_id": 1}))
        self.assertIs(view.func, views.toggle_task_completed)

    def test_app_toggle_task_completed_view_task_not_found_returns_404(self):
        task = self.make_task()
        response = self.client.get(
            reverse("app:toggle_task_completed", kwargs={"task_id": task.id + 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_app_toggle_task_completed_view_marks_task_as_completed(self):
        task = self.make_task()
        response = self.client.post(
            reverse("app:toggle_task_completed", kwargs={"task_id": task.id}),
            data={"completed": "completed"},
        )
        task.refresh_from_db()
        self.assertTrue(task.completed)
        self.assertEqual(response.status_code, 302)

    def test_app_toggle_task_completed_view_marks_task_as_not_completed(self):
        task = self.make_task(completed=True)
        response = self.client.post(
            reverse("app:toggle_task_completed", kwargs={"task_id": task.id})
        )
        task.refresh_from_db()

        self.assertFalse(task.completed)
        self.assertEqual(response.status_code, 302)

    def test_app_toggle_task_completed_view_get_request_does_not_change_task_status(
        self,
    ):
        task = self.make_task()
        response = self.client.get(
            reverse("app:toggle_task_completed", kwargs={"task_id": task.id})
        )
        task.refresh_from_db()

        self.assertFalse(task.completed)
        self.assertEqual(response.status_code, 302)
