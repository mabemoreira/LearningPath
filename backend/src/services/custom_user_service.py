from django.contrib.auth.models import User
from src.models.custom_user import (
    CustomUser,
    CustomUserSerializer,
    UserSerializer,
)


def create_custom_user(data: dict) -> dict:
    UserSerializer(data=data).is_valid(raise_exception=True)
    user = User.objects.create_user(**data)
    custom_user = CustomUser.objects.create(user=user)
    custom_user.save()  # salva no BD
    return CustomUserSerializer(custom_user).data
