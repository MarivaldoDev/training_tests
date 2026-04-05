import logging

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView

from utils.functions import list_errors

from .forms import RegisterForm

logger = logging.getLogger(__name__)


class RegisterView(FormView):
    template_name = "authors/pages/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("authors:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)


class MyLoginView(LoginView):
    template_name = "authors/pages/login.html"

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:tasks", kwargs={"author_id": self.request.user.id})


def logout_view(request):
    logout(request)
    return redirect("tasks:home")
