from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/category/<int:category_id>/", views.tasks_by_category, name="tasks_by_category"),
    path("tasks/", views.task_list, name="tasks"),
    path("categories/", views.category_list, name="categories"),
]
