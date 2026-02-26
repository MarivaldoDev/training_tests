import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import RegisterForm

logger = logging.getLogger(__name__)


def register_view(request):
    logger.info("Acessando a página de registro.")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("authors:login")
        else:
            for error in form.errors:
                message = form.errors[error].as_text().replace("* ", "")
                messages.error(request, message)
    else:
        form = RegisterForm()

    return render(request, "authors/pages/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("tasks:tasks", user.id)
        else:
            for error in form.errors:
                message = form.errors[error].as_text().replace("* ", "")
                messages.error(request, message)
    else:
        form = AuthenticationForm()

    return render(request, "authors/pages/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("tasks:home")
