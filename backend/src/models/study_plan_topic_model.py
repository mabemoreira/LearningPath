from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel
from src.models.study_plan_model import StudyPlan, StudyPlanSerializer


class StudyPlanTopic(BaseModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    study_plan = models.OneToOneField(
        StudyPlan, on_delete=models.CASCADE, blank=False, null=False
    )


class StudyPlanTopicSerializer(serializers.ModelSerializer):
    study_plan = StudyPlanSerializer(many=False, read_only=True, fields=["id", "title"])

    class Meta:
        model = StudyPlanTopic
        fields = ["id", "title", "description", "study_plan"]
