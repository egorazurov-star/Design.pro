from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь портала: стандартные поля Django + ФИО."""
    full_name = models.CharField('ФИО', max_length=150, blank=True)

    def __str__(self):
        return self.username
