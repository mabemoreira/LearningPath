from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel
from src.models.study_plan_model import StudyPlan, StudyPlanSerializer


class StudyPlanTopic(BaseModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    study_plan = models.ForeignKey(
        StudyPlan, on_delete=models.CASCADE, blank=False, null=False
    )


class StudyPlanTopicSerializer(serializers.ModelSerializer):
    study_plan = serializers.SerializerMethodField("get_study_plan")

    class Meta:
        model = StudyPlanTopic
        fields = ["id", "title", "description", "study_plan"]

    def get_study_plan(self, obj):
        study_plan_info = {"id": obj.study_plan.id, "plan_title": obj.study_plan.title}
        return study_plan_info
