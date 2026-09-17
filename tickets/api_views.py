from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ticket
from .serializers import TicketSerializer


class TicketListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "admin":
            tickets = Ticket.objects.all().order_by("-created_at")
        else:
            tickets = Ticket.objects.filter(
                created_by=request.user
            ).order_by("-created_at")

        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            ticket = serializer.save(
                created_by=request.user
            )

            return Response(
                TicketSerializer(ticket).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class TicketDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            request.user.role != "admin"
            and ticket.created_by != request.user
        ):
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TicketSerializer(ticket)

        return Response(serializer.data)


class TicketStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, ticket_id):
        if request.user.role != "admin":
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")

        if new_status not in [
            "new",
            "in_progress",
            "closed",
        ]:
            return Response(
                {"error": "Invalid status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ticket.status = new_status
        ticket.save()

        return Response(
            {
                "message": "Status updated successfully.",
                "status": ticket.status,
            },
            status=status.HTTP_200_OK,
        )
class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            request.user.role != "admin"
            and ticket.created_by != request.user
        ):
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = request.data.get("message")

        if not message:
            return Response(
                {"error": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from .models import Comment

        comment = Comment.objects.create(
            ticket=ticket,
            user=request.user,
            message=message,
        )

        return Response(
            {
                "id": comment.id,
                "ticket": ticket.id,
                "user": request.user.username,
                "message": comment.message,
                "created_at": comment.created_at,
            },
            status=status.HTTP_201_CREATED,
        )
class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role != "admin" and ticket.created_by != request.user:
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = request.data.get("message")

        if not message:
            return Response(
                {"error": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from .models import Comment

        comment = Comment.objects.create(
            ticket=ticket,
            user=request.user,
            message=message,
        )

        return Response(
            {
                "id": comment.id,
                "ticket": ticket.id,
                "user": request.user.username,
                "message": comment.message,
                "created_at": comment.created_at,
            },
            status=status.HTTP_201_CREATED,
        )
class AdminTicketListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        tickets = Ticket.objects.all().order_by("-created_at")

        username = request.query_params.get("username")

        if username:
            tickets = tickets.filter(
                created_by__username__icontains=username
            )

        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data)