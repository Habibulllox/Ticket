from django.urls import path



from .views import (
    admin_ticket_list,
    comment_create,
    ticket_create,
    ticket_detail,
    ticket_list,
    ticket_update_status,
)


urlpatterns = [
    path("", ticket_list, name="ticket_list"),

    path("create/", ticket_create, name="ticket_create"),

    path(
        "admin/",
        admin_ticket_list,
        name="admin_ticket_list",
    ),

    path(
        "<int:ticket_id>/",
        ticket_detail,
        name="ticket_detail",
    ),

    path(
        "<int:ticket_id>/comment/",
        comment_create,
        name="comment_create",
    ),

    path(
        "<int:ticket_id>/status/",
        ticket_update_status,
        name="ticket_update_status",
    ),




]