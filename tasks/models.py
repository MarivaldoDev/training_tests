from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    start_date = models.DateField()
    finish_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="task_images/%Y/%m/%d/", blank=True, null=True)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {'Completed' if self.completed else 'Not Completed'}"
