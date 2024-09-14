from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from src.models import BaseModel


class CustomUser(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # ja inclui nome, email, senha


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
