from django.urls import path

from src.controllers.user_controller import UserController

urlpatterns = [
    path("user/", UserController.as_view()),
]
