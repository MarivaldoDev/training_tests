from django.contrib import messages
from django.core.paginator import Paginator


def list_errors(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, error)


def pagination(request, queryset, per_page=5):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj
