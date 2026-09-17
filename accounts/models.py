from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("client", "Client"),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="client",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username