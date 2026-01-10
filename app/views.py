from django.shortcuts import render, get_object_or_404

from .models import Category, Task
from django.db.models import Count, Q


def home(request):
    return render(request, "home.html")


def tasks_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.tasks.filter(
        completed=False
    ).order_by("start_date")
    return render(request, "tasks.html", {"tasks": tasks, "category": category})


def task_list(request):
    tasks = Task.objects.filter(
        completed=False
    ).order_by("start_date")
    return render(request, "tasks.html", {"tasks": tasks})


def category_list(request):
    categories = (
        Category.objects.annotate(
            incomplete_count=Count("tasks", filter=Q(tasks__completed=False))
        )
        .filter(incomplete_count__gt=0)
    )

    return render(request, "categories.html", {"categories": categories})