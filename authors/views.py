from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("authors:register")
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = RegisterForm()

    return render(request, "authors/pages/register.html", {"form": form})
