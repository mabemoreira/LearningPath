from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel


class CustomUser(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # ja inclui nome, email, senha


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class CustomUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = CustomUser
        fields = ["id", "user"]

    def get_user(self, obj):
        user_info = {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
        }
        return user_info
