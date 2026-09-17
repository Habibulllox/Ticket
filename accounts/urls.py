from django.urls import path

from .api_views import RegisterAPIView, LoginAPIView
from .views import (
    login_view,
    logout_view,
    register_view,
    dashboard_view,
)

urlpatterns = [
    # ===== HTML sahifalar =====
    path("", dashboard_view, name="dashboard"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    # ===== API =====
    path(
        "api/auth/register/",
        RegisterAPIView.as_view(),
        name="api_register",
    ),
    path(
        "api/auth/login/",
        LoginAPIView.as_view(),
        name="api_login",
    ),
]