import logging

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Task

logger = logging.getLogger(__name__)


def home(request):
    logger.info("Acessando a página inicial.")
    return render(request, "home.html")


def tasks_by_category(request, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.tasks.filter(completed=False).order_by("start_date")
    return render(request, "tasks.html", {"tasks": tasks, "category": category})


def task_list(request):
    tasks = Task.objects.filter(completed=False).order_by("start_date")
    return render(request, "tasks.html", {"tasks": tasks})


def category_list(request):
    categories = Category.objects.annotate(
        incomplete_count=Count("tasks", filter=Q(tasks__completed=False))
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
