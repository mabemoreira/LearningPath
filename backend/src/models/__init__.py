from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField()
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField()
