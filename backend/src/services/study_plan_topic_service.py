from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from src.exceptions.business_rules_exceptions import DomainDoesNotExist
from src.models.custom_user_model import CustomUser
from src.models.domain_model import Domain
from src.models.study_plan_model import StudyPlan, StudyPlanSerializer
from src.models.study_plan_topic_model import StudyPlanTopic, StudyPlanTopicSerializer

from ..models.user_does_study_plan_and_topic_model import UserDoesStudyPlanAndTopic
from ..models.user_follows_study_plan_model import UserFollowsStudyPlan


def create_study_plan_topic(data: dict, study_plan_id: int) -> StudyPlanTopic:
    """

    Returns:
        dict: dados do tópico criado

    Raises:
        ValidationError: se os dados forem inválidos.
    """

    # verifica se os dados sao validos
    StudyPlanTopicSerializer(data=data).is_valid(raise_exception=True)

    # cria o topico do plano de estudos
    study_plan_topic = StudyPlanTopic.objects.create(
        title=data["title"],
        description=data["description"],
        study_plan_id=study_plan_id,
    )

    # cria relacao de "does" para usuarios que seguem o plano
    for follow in UserFollowsStudyPlan.objects.filter(study_plan_id=study_plan_id):
        user = follow.user
        UserDoesStudyPlanAndTopic.objects.create(
            user_id=user.id, study_plan_topic_id=study_plan_topic.id
        )

    # salva e retorna os dados serializados
    study_plan_topic.save()

    return StudyPlanTopicSerializer(study_plan_topic).data


def check_permission_topic(study_plan_topic: StudyPlanTopic, user: User) -> None:
    """
    Raises:
        PermissionDenied: se o usuário não tiver permissão para acessar o tópico
    """
    if not study_plan_topic.study_plan.access_allowed(user):
        raise PermissionDenied(
            "Você não tem permissão para acessar este tópico do plano de estudos."
        )


def read_study_plan_topic(study_plan_topic_id: int, user: User) -> dict:
    """

    Returns:
        dict: dados do tópico do plano de estudos

    Raises:
        ObjectDoesNotExist: se o tópico do plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para acessar o tópico
    """

    # busca o tópico do plano de estudos, se nao existir gera uma excessao
    study_plan_topic = StudyPlanTopic.objects.get(id=study_plan_topic_id)

    # gera uma excessao se usuario nao tiver permissao para acessar o tópico
    check_permission_topic(study_plan_topic, user)

    # dados serializados
    return StudyPlanTopicSerializer(study_plan_topic).data


def delete_study_plan_topic(study_plan_topic_id: int, user: User) -> None:
    """
    Deleta o tópico do plano de estudos com o id passado.

    Params:
        study_plan_topic_id: id do tópico do plano de estudos
        user: usuário

    Raises:
        ObjectDoesNotExist: se o tópico do plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para deletar o tópico
    """

    # busca o tópico do plano de estudos, se nao existir gera uma excessao
    study_plan_topic = StudyPlanTopic.objects.get(id=study_plan_topic_id)

    # gera uma excessao se usuario nao tiver permissao para deletar o tópico
    check_permission_topic(study_plan_topic, user)

    # deleta o tópico
    study_plan_topic.delete()


def update_study_plan_topic(study_plan_topic_id: int, data: dict, user: User) -> dict:
    """
    Returns:
        dict: dados do tópico do plano de estudos atualizados

    Raises:
        ObjectDoesNotExist: se o tópico do plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para atualizar o tópico
    """

    # busca o tópico do plano de estudos, se nao existir gera uma excessao
    study_plan_topic = StudyPlanTopic.objects.get(id=study_plan_topic_id)

    # gera uma excessao se usuario nao tiver permissao para atualizar o tópico
    check_permission_topic(study_plan_topic, user)

    # verifica se os dados sao validos
    StudyPlanTopicSerializer(study_plan_topic, data=data).is_valid(raise_exception=True)

    # atualiza os dados e salva
    study_plan_topic.title = data["title"]
    study_plan_topic.description = data["description"]
    study_plan_topic.save()

    return StudyPlanTopicSerializer(study_plan_topic).data
