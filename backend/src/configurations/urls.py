from django.contrib import admin
from django.urls import path
from src.controllers.custom_user_controller import UserController

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", UserController.as_view()),
    path("user/<int:user_id>/", UserController.as_view()),
]
