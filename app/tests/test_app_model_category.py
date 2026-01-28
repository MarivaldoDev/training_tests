from django.core.exceptions import ValidationError

from .test_base_app import AppTestBase


class AppCategoryModelTests(AppTestBase):
    def setUp(self):
        self.category = self.make_category(name="Work")
        return super().setUp()

    def test_app_model_category_str_method(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_app_model_category_name_max_length_is_100_chars(self):
        self.category.name = "A" * 101
        with self.assertRaises(ValidationError):
            self.category.full_clean()
