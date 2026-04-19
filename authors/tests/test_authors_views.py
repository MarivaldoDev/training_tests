from django.test import TestCase
from django.urls import reverse

from authors.models import Author


class AuthorsViewsTests(TestCase):
    def test_authors_register_view_returns_error_message_on_invalid_form(self):
        response = self.client.post(reverse("authors:register"), data={})
        content = response.content.decode("utf-8")

        self.assertIn("Todos os campos são obrigatórios.", content)

    def test_authors_register_view_loads_blank_form_if_request_is_get(self):
        response = self.client.get(reverse("authors:register"))
        form = response.context["form"]

        self.assertFalse(form.is_bound)

    def test_authors_login_view_returns_error_message_on_invalid_form(self):
        response = self.client.post(reverse("authors:login"), data={})
        content = response.content.decode("utf-8")

        self.assertIn("Este campo é obrigatório.", content)

    def test_authors_logout_view_logs_out_user_and_redirects_to_home(self):
        user = Author.objects.create(username="testuser", password="testpassword")
        self.client.force_login(user)
        response = self.client.get(reverse("authors:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:home"))
