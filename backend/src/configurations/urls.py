from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from src.controllers.custom_user_controller import UserController
from src.controllers.domain_controller import DomainController
from src.controllers.login_controller import LoginView
from src.controllers.logout_controller import LogoutView

urlpatterns = [
    # Django admin view
    path("admin/", admin.site.urls),
    # User endpoints
    path("user/", UserController.as_view(http_method_names=["post"])),
    path(
        "user/<int:user_id>/",
        UserController.as_view(http_method_names=["put", "get", "delete"]),
    ),
    # Domain endpoints
    path("domain/<int:domain_id>/", DomainController.as_view(http_method_names=["get"])),
    # Authentication endpoints
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    # Swagger
    path("swagger/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
]
