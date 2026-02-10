from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "tasks/category/<int:category_id>/",
        views.tasks_by_category,
        name="tasks_by_category",
    ),
    path("tasks/", views.task_list, name="tasks"),
    path("categories/", views.category_list, name="categories"),
    path("tasks/details/<int:task_id>/", views.task_detail, name="task_detail"),
    path(
        "tasks/details/<int:task_id>/toggle/",
        views.toggle_task_completed,
        name="toggle_task_completed",
    ),
]
