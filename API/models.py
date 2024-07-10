from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField(max_length=20)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
        