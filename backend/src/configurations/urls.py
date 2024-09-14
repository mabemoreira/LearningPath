from django.urls import path

from backend.src.controllers.custom_user_controller import UserController

urlpatterns = [
    path("user/", UserController.as_view()),
]
