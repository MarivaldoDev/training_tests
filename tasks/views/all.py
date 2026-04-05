import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from ..models import Category, Task

logger = logging.getLogger(__name__)


def home(request):
    logger.info("Acessando a página inicial.")
    return render(request, "home.html")


@login_required(login_url="authors:login")
def tasks_by_category(request, author_id: int, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.tasks.filter(author_id=author_id, completed=False).order_by(
        "start_date"
    )
    return render(request, "tasks.html", {"tasks": tasks, "category": category})


@login_required(login_url="authors:login")
def task_list(request, author_id: int):
    tasks = Task.objects.filter(author_id=author_id, completed=False).order_by(
        "start_date"
    )
    return render(request, "tasks.html", {"tasks": tasks})


@login_required(login_url="authors:login")
def category_list(request, author_id: int):
    categories = Category.objects.annotate(
        incomplete_count=Count(
            "tasks", filter=Q(tasks__author_id=author_id, tasks__completed=False)
        )
    ).filter(incomplete_count__gt=0)

    return render(
        request, "categories.html", {"categories": categories, "author_id": author_id}
    )


@login_required(login_url="authors:login")
def task_detail(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id, author=request.user)
    return render(request, "task_detail.html", {"task": task})


@login_required(login_url="authors:login")
def dashboard(request, author_id: int):
    return render(request, "dashboard.html", {"author_id": author_id})
