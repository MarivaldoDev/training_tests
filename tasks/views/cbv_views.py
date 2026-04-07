from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors

from ..forms import CategoryForm, TaskForm, TaskUpdateForm
from ..models import Category, Task


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
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


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "update_task.html"

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"task_id": self.object.id})


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class DeleteTask(DeleteView):
    model = Task
    template_name = "task_detail.html"

    def get_success_url(self):
        return reverse("tasks:tasks", kwargs={"author_id": self.object.author.id})


def toggle_task_completed(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id, author=request.user)

    if request.method == "POST":
        task.completed = "completed" in request.POST
        task.finish_date = datetime.now().date() if task.completed else None
        task.save()

    return redirect("tasks:task_detail", task_id=task.id)


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class CreateCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "create_category.html"

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:categories", kwargs={"author_id": self.request.user.id})
