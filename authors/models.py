import logging

from decouple import config
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

logger = logging.getLogger(__name__)


class Author(AbstractUser):
    image_profile = models.ImageField(
        upload_to="author_images/%Y/%m/", blank=True, null=True
    )

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new and self.email:
            subject = "Bem-vindo ao Task Manager!"
            dominio = config("DOMAIN_NAME", default="http://localhost:8000")
            login_url = reverse("authors:login")
            message = (
                f"Olá {self.first_name},\n\n"
                "Bem-vindo ao Task Manager!\n\n"
                "Sua conta foi criada com sucesso. Para acessar a plataforma, "
                f"clique no link abaixo:\n\n"
                f"{dominio}{login_url}\n\n"
                "Usuário: " + self.username + "\n\n"
                "Se você não realizou este cadastro, ignore este e-mail.\n\n"
                "Atenciosamente,\n"
                "Equipe do Task Manager"
            )
            from_email = config("EMAIL_HOST_USER")
            try:
                self.email_user(subject, message, from_email)
                logger.info(f"Email de boas-vindas enviado para {self.username}")
            except Exception as e:
                logger.error(
                    f"Erro ao enviar email de boas-vindas para {self.username}: {e}"
                )

    def __str__(self):
        return self.username
