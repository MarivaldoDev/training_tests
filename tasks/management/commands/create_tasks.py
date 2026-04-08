from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tasks.models import Category, Task


class Command(BaseCommand):
    help = "Cria um usuário de teste e 20 tarefas associadas a ele."

    def handle(self, *args, **options):
        user = User.objects.create_user(username="testuser", password="testpassword")
        category = Category.objects.create(name="Test")

        for _ in range(20):
            Task.objects.create(
                title="Test Task",
                description="This is a test task.",
                start_date="2024-01-01",
                completed=False,
                author=user,
                category=category,
            )

        self.stdout.write(self.style.SUCCESS("Usuário e tarefas criados com sucesso!"))
