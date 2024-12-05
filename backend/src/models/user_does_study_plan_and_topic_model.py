from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel
from src.models.custom_user_model import CustomUser, User
from src.models.domain_model import Domain, DomainSerializer
from src.models.study_plan_model import StudyPlan
from src.models.study_plan_topic_model import StudyPlanTopic


class UserDoesStudyPlanAndTopic(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, blank=False
    )
    study_plan_topic = models.ForeignKey(
        StudyPlanTopic, on_delete=models.CASCADE, null=False, blank=False
    )
    done = models.BooleanField(default=False)


class UserDoesStudyPlanAndTopicSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")
    study_plan_topic = serializers.SerializerMethodField("get_study_plan_topic")

    class Meta:
        model = UserDoesStudyPlanAndTopic
        fields = ["id", "user", "done", "study_plan_topic"]

    def get_user(self, obj):
        user_info = {"id": obj.user.id, "username": obj.user.user.username}
        return user_info

    def get_study_plan_topic(self, obj):
        study_plan_topic_info = {
            "id": obj.study_plan_topic.id,
            "title": obj.study_plan_topic.title,
            "description": obj.study_plan_topic.description,
            "study_plan": obj.study_plan_topic.study_plan.id,
        }
        return study_plan_topic_info

    def save(self, **kwargs) -> bool:
        return super().save(**kwargs)
