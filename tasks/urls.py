from django.urls import path

from .views import views_category, views_tasks

app_name = "tasks"

urlpatterns = [
    path("", views_category.home, name="home"),
    path("dashboard/<int:author_id>/", views_category.dashboard, name="dashboard"),
    path("tasks/create/", views_tasks.CreateTask.as_view(), name="create_task"),
    path(
        "tasks/update/<int:pk>/",
        views_tasks.UpdateTask.as_view(),
        name="update_task",
    ),
    path(
        "tasks/delete/<int:pk>/",
        views_tasks.DeleteTask.as_view(),
        name="delete_task",
    ),
    path(
        "tasks/category/<int:author_id>/<int:category_id>/",
        views_tasks.tasks_by_category,
        name="tasks_by_category",
    ),
    path("tasks/<int:author_id>/", views_tasks.task_list, name="tasks"),
    path(
        "categories/<int:author_id>/", views_category.category_list, name="categories"
    ),
    path(
        "categories/create/",
        views_category.CreateCategory.as_view(),
        name="create_category",
    ),
    path("tasks/details/<int:task_id>/", views_tasks.task_detail, name="task_detail"),
    path(
        "tasks/details/<int:task_id>/toggle/",
        views_tasks.toggle_task_completed,
        name="toggle_task_completed",
    ),
]
