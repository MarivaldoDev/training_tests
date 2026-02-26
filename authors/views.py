import logging

from django.contrib import messages
from django.contrib.auth import login
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
                messages.error(request, form.errors[error])
    else:
        form = RegisterForm()

    return render(request, "authors/pages/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("authors:login")
        else:
            for error in form.errors:
                logger.debug(
                    f"Erro de validação no formulário de login: {form.errors[error]}"
                )
                messages.error(request, form.errors[error])
    else:
        form = AuthenticationForm()

    return render(request, "authors/pages/login.html", {"form": form})
