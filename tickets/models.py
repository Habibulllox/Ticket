from django.conf import settings
from django.db import models


class Ticket(models.Model):
    STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("normal", "Normal"),
        ("high", "High"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(
        upload_to="tickets/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="normal",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ticket.title}"