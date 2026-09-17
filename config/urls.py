from django.contrib import admin
from django.urls import include, path

from tickets.api_views import (
    TicketDetailAPIView,
    TicketListCreateAPIView,
    TicketStatusUpdateAPIView,
    CommentCreateAPIView,
    AdminTicketListAPIView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),

    path("tickets/", include("tickets.urls")),

    path(
        "api/tickets/",
        TicketListCreateAPIView.as_view(),
        name="api_ticket_list",
    ),
    path(
        "api/admin/tickets/",
        AdminTicketListAPIView.as_view(),
        name="api_admin_tickets",
    ),

    path(
        "api/tickets/<int:ticket_id>/comment/",
        CommentCreateAPIView.as_view(),
        name="api_ticket_comment",
    ),

    path(
        "api/tickets/<int:ticket_id>/",
        TicketDetailAPIView.as_view(),
        name="api_ticket_detail",
    ),
]