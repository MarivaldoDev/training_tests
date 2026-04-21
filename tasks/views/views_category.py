import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors

from ..decorators.decorator import user_only
from ..forms import CategoryForm, CategoryUpdateForm
from ..models import Category

logger = logging.getLogger(__name__)


def home(request):
    logger.info("Acessando a página inicial.")
    return render(request, "home.html")


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class CreateCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "create_category.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:categories")


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class UpdateCategory(UpdateView):
    model = Category
    form_class = CategoryUpdateForm
    template_name = "update_category.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def form_valid(self, form):
        if not form.has_changed():
            return redirect(self.get_success_url())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:dashboard")


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class DeleteCategory(DeleteView):
    model = Category
    template_name = "categories.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse("tasks:dashboard")


@login_required(login_url="authors:login")
@user_only
def category_list(request):
    categories = Category.objects.annotate(
        incomplete_count=Count(
            "tasks", filter=Q(tasks__author=request.user.id, tasks__completed=False)
        )
    ).filter(incomplete_count__gt=0)

    return render(request, "categories.html", {"categories": categories})


@login_required(login_url="authors:login")
@user_only
def dashboard(request):
    return render(request, "dashboard.html")
