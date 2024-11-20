from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers
from src.models.base_model import BaseModel
from src.models.custom_user_model import CustomUser, User
from src.models.domain_model import Domain, DomainSerializer

from .user_follows_study_plan_model import UserFollowsStudyPlan


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

    def is_private(self):
        """
        Verifica se o plano de estudos é privado.

        Returns:
            bool: True se o plano de estudos é privado, False caso contrário
        """
        return self.visibility.name == "private"

    def set_visibility(self, visibility):
        """
        Define a visibilidade do plano de estudos.

        Params:
            visibility: visibilidade do plano de estudos

        Raises:
            ObjectDoesNotExist: se a visibilidade não existir
        """
        self.visibility = Domain.objects.get(
            name=visibility, type="visibility", relationship="StudyPlan"
        )

    def access_allowed(self, user: User) -> bool:
        """Verifica se o usuário tem permissão para acessar o plano de estudos.

        Params:
            study_plan: plano de estudos
            user: usuário

        Returns:
            bool: True se o usuário tem permissão, False caso contrário
        """
        # plano foi deletado e usuario nao o segue
        if (
            self.deleted
            and not UserFollowsStudyPlan.objects.filter(
                user=user,
                study_plan=self,
            ).exists()
        ):
            return False
        # plano eh privado e usuario nao eh o autor
        elif self.is_private() and not self.author.id == user.id:
            return False
        return True


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

    def save(self, **kwargs) -> bool:
        """
        Salva o objeto no banco de dados.

        Returns:
            bool: True se o objeto foi salvo, False caso contrário
        """
        return super().save(**kwargs)
