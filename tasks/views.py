import logging

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Category, Task

logger = logging.getLogger(__name__)


def home(request):
    logger.info("Acessando a página inicial.")
    return render(request, "home.html")


def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect("tasks:tasks", request.user.id)
        else:
            for error in form.errors:
                message = form.errors[error].as_text().replace("* ", "")
                messages.error(request, message)
    else:
        form = TaskForm()

    return HttpResponse(form.as_div())


def tasks_by_category(request, author_id: int, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.tasks.filter(author_id=author_id, completed=False).order_by(
        "start_date"
    )
    return render(request, "tasks.html", {"tasks": tasks, "category": category})


def task_list(request, author_id: int):
    tasks = Task.objects.filter(author_id=author_id, completed=False).order_by(
        "start_date"
    )
    return render(request, "tasks.html", {"tasks": tasks})


def category_list(request, author_id: int):
    categories = Category.objects.annotate(
        incomplete_count=Count(
            "tasks", filter=Q(tasks__author_id=author_id, tasks__completed=False)
        )
    ).filter(incomplete_count__gt=0)

    return render(request, "categories.html", {"categories": categories})


def task_detail(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "task_detail.html", {"task": task})


def toggle_task_completed(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.completed = "completed" in request.POST
        task.save()
    return redirect("tasks:task_detail", task_id=task.id)
