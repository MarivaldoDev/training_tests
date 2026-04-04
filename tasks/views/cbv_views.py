from datetime import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from ..forms import CategoryForm, TaskForm, TaskUpdateForm
from ..models import Task


class CreateTask(View):
    def render_form(self, form):
        return render(self.request, "create_task.html", {"form": form})

    def get(self, request):
        form = TaskForm()
        return self.render_form(form)

    def post(self, request):
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect("tasks:tasks", request.user.id)
        else:
            for error in form.errors:
                message = form.errors[error].as_text().replace("* ", "")
                messages.error(request, message)

        return self.render_form(form)


class UpdateTask(View):
    def render_form(self, form, task):
        return render(self.request, "update_task.html", {"form": form, "task": task})

    def get_task(self, task_id):
        task = get_object_or_404(Task, pk=task_id)
        return task

    def get(self, request, task_id):
        task = self.get_task(task_id)
        form = TaskForm(instance=task)

        return self.render_form(form, task)

    def post(self, request, task_id):
        task = self.get_task(task_id)
        form = TaskUpdateForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:task_detail", task_id=task_id)
        else:
            for error in form.errors:
                message = form.errors[error].as_text().replace("* ", "")
                messages.error(request, message)

        return self.render_form(form, task)


class DeleteTask(UpdateTask):
    def post(self, request, task_id):
        task = self.get_task(task_id)
        task.delete()
        return redirect("tasks:tasks", request.user.id)


class ToggleTaskCompleted(UpdateTask):
    def post(self, request, task_id):
        task = self.get_task(task_id)
        if "completed" in request.POST:
            task.completed = True
            task.finish_date = datetime.now().date()
        task.save()

        return redirect("tasks:task_detail", task_id=task_id)


class CreateCategory(View):
    def render_form(self, form):
        return render(self.request, "create_category.html", {"form": form})

    def get(self, request):
        form = CategoryForm()
        return self.render_form(form)

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:categories", request.user.id)
        else:
            for error in form.errors:
                message = form.errors[error].as_text().replace("* ", "")
                messages.error(request, message)

        return self.render_form(form)
