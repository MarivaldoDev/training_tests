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
            "completed",
        )
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
                attrs={"class": "form-control", "type": "date"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        # cleaned_data = super().clean()
        # title = cleaned_data.get("title")
        # description = cleaned_data.get("description")
        # category = cleaned_data.get("category")
        # start_date = cleaned_data.get("start_date")
        # image = cleaned_data.get("image")
        # completed = cleaned_data.get("completed")

        pass


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
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
        elif Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Essa categoria já existe.")

        return cleaned_data
