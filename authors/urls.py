from django.urls import path

from . import views

app_name = "authors"

urlpatterns = [
    path("register/create/", views.RegisterView.as_view(), name="register"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
