from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/<int:author_id>/", views.dashboard, name="dashboard"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/update/<int:task_id>/", views.update_task, name="update_task"),
    path(
        "tasks/category/<int:author_id>/<int:category_id>/",
        views.tasks_by_category,
        name="tasks_by_category",
    ),
    path("tasks/<int:author_id>/", views.task_list, name="tasks"),
    path("categories/<int:author_id>/", views.category_list, name="categories"),
    path("tasks/details/<int:task_id>/", views.task_detail, name="task_detail"),
    path(
        "tasks/details/<int:task_id>/toggle/",
        views.toggle_task_completed,
        name="toggle_task_completed",
    ),
]
