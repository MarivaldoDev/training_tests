from django.contrib import messages


def list_errors(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, error)
