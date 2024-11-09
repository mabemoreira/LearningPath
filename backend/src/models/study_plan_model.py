from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel
from src.models.custom_user_model import CustomUser, CustomUserSerializer
from src.models.domain_model import Domain, DomainSerializer


class StudyPlan(BaseModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    visibility = models.OneToOneField(Domain)
    author = models.OneToOneField(CustomUser)
    deleted = models.BooleanField(default=False)


class StudyPlanSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(
        many=False, read_only=True, fields=["id", "username", "email"]
    )
    domain = DomainSerializer(many=False, read_only=True)

    class Meta:
        model = StudyPlan
        fields = ["id", "title", "visibility", "author", "deleted"]
