from django import forms

from .models import Category, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "category",
            "start_date",
            "image",
        )

        labels = {
            "title": "Título",
            "description": "Descrição",
            "category": "Categoria",
            "start_date": "Data de Início",
            "image": "Imagem (opcional)",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Título da tarefa"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descrição da tarefa",
                    "rows": 4,
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control-file", "accept": "image/*"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        start_date = cleaned_data.get("start_date")

        if not title and not start_date:
            raise forms.ValidationError(
                "Preencha pelo menos o título ou a data de início."
            )
        elif Task.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Já existe uma tarefa com esse título.")

        return cleaned_data


class TaskUpdateForm(TaskForm):
    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
        return task


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        labels = {
            "name": "Nome",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome da categoria"}
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if not name:
            raise forms.ValidationError("O nome da categoria é obrigatório.")
        elif Category.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Essa categoria já existe.")

        return cleaned_data


class CategoryUpdateForm(CategoryForm):
    def save(self, commit=True):
        category = super().save(commit=False)
        if commit:
            category.save()
        return category
