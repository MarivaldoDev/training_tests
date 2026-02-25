from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Seu nome de usuário"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Digite seu e-mail"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Crie sua senha"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not username or not email or not password:
            raise forms.ValidationError("Todos os campos são obrigatórios.")

        elif len(password) < 6:
            raise forms.ValidationError("A senha deve conter pelo menos 6 caracteres.")

        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse e-mail já está em uso.")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "Digite seu e-mail"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Digite sua senha"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            raise forms.ValidationError("Todos os campos são obrigatórios.")

        elif not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "E-mail ou senha inválidos. Certifiqui-se que as credenciais estão corretas ou se realmente criou uma conta."
            )

        return cleaned_data
