from rest_framework import serializers

from .models import Ticket, Comment


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "title",
            "description",
            "image",
            "status",
            "priority",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "ticket",
            "user",
            "message",
            "created_at",
        )
        read_only_fields = (
            "id",
            "ticket",
            "user",
            "created_at",
        )