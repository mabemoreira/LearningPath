from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel


class Domain(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(max_length=255, blank=False, null=False)
    relationship = models.CharField(max_length=255, blank=False, null=False)


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "name", "type", "relationship"]
