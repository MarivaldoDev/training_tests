from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="categories"),
    path("categories/<int:category_id>/", views.tasks_by_category, name="category_tasks"),
    path("tasks/", views.task_list, name="tasks"),
]
