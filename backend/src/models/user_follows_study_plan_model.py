from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel
from src.models.custom_user_model import CustomUser, User
from src.models.domain_model import Domain, DomainSerializer
from src.models.study_plan_model import StudyPlan


class UserFollowsStudyPlan(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, blank=False
    )
    study_plan = models.ForeignKey(
        StudyPlan, on_delete=models.CASCADE, null=False, blank=False
    )
    progress = models.FloatField(default=0)
    time_spent = models.FloatField(default=0)


class UserFollowsStudyPlanSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")
    study_plan = serializers.SerializerMethodField("get_study_plan")

    class Meta:
        model = UserFollowsStudyPlan
        fields = ["id", "user", "study_plan", "progress", "time_spent"]

    def get_user(self, obj):
        user_info = {"id": obj.user.id, "username": obj.author.user.username}
        return user_info

    def get_study_plan(self, obj):
        study_plan_info = {
            "id": obj.study_plan.id,
            "title": obj.study_plan.title,
            "visibility": obj.study_plan.visibility.name,
            "author": obj.study_plan.author.user.username,
        }
        return study_plan_info

    def save(self, **kwargs) -> bool:
        return super().save(**kwargs)
