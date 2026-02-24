from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("authors:register")
    else:
        form = RegisterForm()

    return render(request, "authors/pages/register.html", {"form": form})
