import logging
from functools import wraps

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from tasks.models import Task

logger = logging.getLogger(__name__)


def user_only(view_func):
    """
    Permite o usuário acessar apenas suas próprias informações.
    Evita que usuários acessem dados de outros usuários.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        request_user = request.user
        author_id = kwargs.get("author_id")
        task_id = kwargs.get("task_id") or kwargs.get("pk")

        if author_id is not None:
            target_user = get_object_or_404(User, id=author_id)
        elif task_id is not None:
            task = get_object_or_404(Task, pk=task_id)
            target_user = task.author
        else:
            return redirect("tasks:home")

        if request_user != target_user:
            logger.warning(
                f"{request_user.username} tentou acessar dados de outro usuário: {target_user.username}"
            )
            return redirect("tasks:home")

        return view_func(request, *args, **kwargs)

    return wrapper
