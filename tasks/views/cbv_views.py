from datetime import datetime

from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors

from ..forms import CategoryForm, TaskForm, TaskUpdateForm
from ..models import Category, Task


class CreateTask(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "create_task.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:tasks", kwargs={"author_id": self.object.author.id})


class UpdateTask(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "update_task.html"

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"task_id": self.object.id})


class DeleteTask(DeleteView):
    model = Task
    template_name = "task_detail.html"

    def get_success_url(self):
        return reverse("tasks:tasks", kwargs={"author_id": self.object.author.id})


class ToggleTaskCompleted(UpdateView):
    model = Task
    fields = []  # não precisa de form
    template_name = "task_detail.html"

    def form_valid(self, form):
        task = self.get_object()

        if "completed" in self.request.POST:
            task.completed = True
            task.finish_date = datetime.now()

        task.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"task_id": self.object.id})


class CreateCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "create_category.html"

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:categories", kwargs={"author_id": self.request.user.id})
