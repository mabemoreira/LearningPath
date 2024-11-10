from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel
from src.models.custom_user_model import CustomUser, CustomUserSerializer
from src.models.domain_model import Domain, DomainSerializer


def default_visibility():
    try:
        return Domain.objects.get(name="private", relationship="StudyPlan").id
    except ObjectDoesNotExist:
        raise Exception("Domain 'private' not found")


class StudyPlan(BaseModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    visibility = models.ForeignKey(
        Domain, on_delete=models.SET_DEFAULT, default=default_visibility
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, blank=False
    )
    deleted = models.BooleanField(default=False)


class StudyPlanSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField("get_author")
    visibility = serializers.SerializerMethodField("get_visibility")

    class Meta:
        model = StudyPlan
        fields = ["id", "title", "visibility", "author", "deleted"]

    def get_author(self, obj):
        author_info = {"id": obj.author.id, "username": obj.author.user.username}
        return author_info

    def get_visibility(self, obj):
        visibility_info = {
            "id": obj.visibility.id,
            "name": obj.visibility.name,
            "type": obj.visibility.type,
        }
        return visibility_info
