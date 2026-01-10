from django.shortcuts import render, get_object_or_404

from .models import Category, Task


def home(request):
    return render(request, "home.html")


def category_list(request):
    categories = Category.objects.all().prefetch_related("tasks")
    return render(request, "categories.html", {"categories": categories})


def task_list(request):
    tasks = Task.objects.filter(
        completed=False
    ).order_by("start_date")
    return render(request, "tasks.html", {"tasks": tasks})


def tasks_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.tasks.filter(
        completed=False
    ).order_by("start_date")
    return render(request, "tasks.html", {"tasks": tasks, "category": category})


