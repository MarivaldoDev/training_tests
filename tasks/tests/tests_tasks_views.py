from django.urls import resolve, reverse

from ..views import views_category, views_tasks
from .test_base_tasks import TasksTestBase


class TasksViewsTests(TasksTestBase):
    def test_tasks_home_view_function_is_correct(self):
        view = resolve(reverse("tasks:home"))
        self.assertIs(view.func, views_category.home)

    def test_tasks_tasks_view_function_is_correct(self):
        view = resolve(reverse("tasks:tasks", kwargs={"author_id": 1}))
        self.assertIs(view.func, views_tasks.task_list)

    def test_tasks_category_view_function_is_correct(self):
        view = resolve(reverse("tasks:categories", kwargs={"author_id": 1}))
        self.assertIs(view.func, views_category.category_list)

    def test_tasks_category_view_loads_categories_where_tasks_exist(self):
        self.make_category(name="Category 1")
        self.make_category(name="Category 2")
        self.make_task(category_data={"name": "Category 1"})

        response = self.client.get(reverse("tasks:categories", kwargs={"author_id": 1}))
        content = response.content.decode("utf-8")
        response_context_categories = response.context["categories"]

        self.assertIn("Category 1", content)
        self.assertNotIn("Category 2", content)
        self.assertEqual(len(response_context_categories), 1)

    def test_tasks_tasks_by_category_view_function_is_correct(self):
        view = resolve(
            reverse(
                "tasks:tasks_by_category", kwargs={"author_id": 1, "category_id": 1}
            )
        )
        self.assertIs(view.func, views_tasks.tasks_by_category)

    def test_tasks_tasks_by_category_view_category_not_found_returns_404(self):
        category = self.make_category()
        response = self.client.get(
            reverse(
                "tasks:tasks_by_category",
                kwargs={"author_id": 1, "category_id": category.id + 1},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_tasks_tasks_by_category_view_loads_tasks(self):
        self.make_task(category_data={"name": "Category 1"})
        response = self.client.get(
            reverse(
                "tasks:tasks_by_category", kwargs={"author_id": 1, "category_id": 1}
            )
        )
        content = response.content.decode("utf-8")
        response_context_tasks = response.context["page_obj"]

        self.assertIn("Task 1", content)
        self.assertEqual(len(response_context_tasks), 1)

    def test_tasks_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("tasks:home"))
        self.assertEqual(response.status_code, 200)

    def test_tasks_home_view_loads_correct_template(self):
        response = self.client.get(reverse("tasks:home"))
        self.assertTemplateUsed(response, "home.html")

    def test_tasks_tasks_template_shows_no_tasks_message_when_no_tasks(self):
        response = self.client.get(reverse("tasks:tasks", kwargs={"author_id": 1}))
        self.assertIn(b"<p>Nenhuma tarefa encontrada.</p>", response.content)

    def test_tasks_tasks_template_loads_tasks(self):
        self.make_task()
        response = self.client.get(reverse("tasks:tasks", kwargs={"author_id": 1}))
        content = response.content.decode("utf-8")
        response_context_tasks = response.context["page_obj"]

        self.assertIn("Task 1", content)
        self.assertEqual(len(response_context_tasks), 1)

    def test_tasks_task_detail_view_function_is_correct(self):
        view = resolve(reverse("tasks:task_detail", kwargs={"task_id": 1}))
        self.assertIs(view.func, views_tasks.task_detail)

    def test_tasks_task_detail_view_task_not_found_returns_404(self):
        task = self.make_task()
        response = self.client.get(
            reverse("tasks:task_detail", kwargs={"task_id": task.id + 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_tasks_task_detail_view_loads_task(self):
        task = self.make_task()
        response = self.client.get(
            reverse("tasks:task_detail", kwargs={"task_id": task.id})
        )
        content = response.content.decode("utf-8")
        response_context_task = response.context["task"]

        self.assertIn("Task 1", content)
        self.assertEqual(response_context_task, task)

    def test_tasks_toggle_task_completed_view_function_is_correct(self):
        view = resolve(reverse("tasks:toggle_task_completed", kwargs={"task_id": 1}))
        self.assertIs(view.func, views_tasks.toggle_task_completed)

    def test_tasks_toggle_task_completed_view_task_not_found_returns_404(self):
        task = self.make_task()
        response = self.client.get(
            reverse("tasks:toggle_task_completed", kwargs={"task_id": task.id + 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_tasks_toggle_task_completed_view_marks_task_as_completed(self):
        task = self.make_task()
        response = self.client.post(
            reverse("tasks:toggle_task_completed", kwargs={"task_id": task.id}),
            data={"completed": "completed"},
        )
        task.refresh_from_db()
        self.assertTrue(task.completed)
        self.assertEqual(response.status_code, 302)

    def test_tasks_toggle_task_completed_view_marks_task_as_not_completed(self):
        task = self.make_task(completed=True)
        response = self.client.post(
            reverse("tasks:toggle_task_completed", kwargs={"task_id": task.id})
        )
        task.refresh_from_db()

        self.assertFalse(task.completed)
        self.assertEqual(response.status_code, 302)

    def test_tasks_toggle_task_completed_view_get_request_does_not_change_task_status(
        self,
    ):
        task = self.make_task()
        response = self.client.get(
            reverse("tasks:toggle_task_completed", kwargs={"task_id": task.id})
        )
        task.refresh_from_db()

        self.assertFalse(task.completed)
        self.assertEqual(response.status_code, 302)
