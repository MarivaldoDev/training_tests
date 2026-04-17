from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors, pagination

from ..decorators.decorator import user_only
from ..forms import TaskForm, TaskUpdateForm
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
        return reverse("tasks:tasks")


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "update_task.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def form_valid(self, form):
        if not form.has_changed():
            return redirect(self.get_success_url())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:task_detail")


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class DeleteTask(DeleteView):
    model = Task
    template_name = "task_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse("tasks:tasks")


@login_required(login_url="authors:login")
@user_only
def toggle_task_completed(request, slug: str):
    task = get_object_or_404(Task, slug=slug)

    if request.method == "POST":
        task.completed = "completed" in request.POST
        task.finish_date = datetime.now().date() if task.completed else None
        task.save()

    return redirect("tasks:task_detail", slug=task.slug)


@login_required(login_url="authors:login")
@user_only
def tasks_by_category(request, slug: str):
    category = get_object_or_404(Category, slug=slug)
    tasks = Task.objects.filter(
        author=request.user, category=category, completed=False
    ).order_by("start_date")
    page_obj = pagination(request, tasks, per_page=5)
    return render(request, "tasks.html", {"page_obj": page_obj, "category": category})


@login_required(login_url="authors:login")
@user_only
def task_list(request):
    tasks = Task.objects.filter(author=request.user, completed=False).order_by(
        "start_date"
    )
    page_obj = pagination(request, tasks, per_page=5)
    return render(request, "tasks.html", {"page_obj": page_obj})


@login_required(login_url="authors:login")
@user_only
def task_detail(request, slug: str):
    task = get_object_or_404(Task, author=request.user, slug=slug)
    return render(request, "task_detail.html", {"task": task})
