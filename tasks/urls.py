from django.urls import path

from .views import all, cbv_views

app_name = "tasks"

urlpatterns = [
    path("", all.home, name="home"),
    path("dashboard/<int:author_id>/", all.dashboard, name="dashboard"),
    path("tasks/create/", cbv_views.CreateTask.as_view(), name="create_task"),
    path(
        "tasks/update/<int:pk>/",
        cbv_views.UpdateTask.as_view(),
        name="update_task",
    ),
    path(
        "tasks/delete/<int:pk>/",
        cbv_views.DeleteTask.as_view(),
        name="delete_task",
    ),
    path(
        "tasks/category/<int:author_id>/<int:category_id>/",
        all.tasks_by_category,
        name="tasks_by_category",
    ),
    path("tasks/<int:author_id>/", all.task_list, name="tasks"),
    path("categories/<int:author_id>/", all.category_list, name="categories"),
    path(
        "categories/create/", cbv_views.CreateCategory.as_view(), name="create_category"
    ),
    path("tasks/details/<int:task_id>/", all.task_detail, name="task_detail"),
    path(
        "tasks/details/<int:task_id>/toggle/",
        cbv_views.toggle_task_completed,
        name="toggle_task_completed",
    ),
]
