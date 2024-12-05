import re

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from src.exceptions.business_rules_exceptions import DomainDoesNotExist
from src.models.custom_user_model import CustomUser
from src.models.domain_model import Domain
from src.models.study_plan_model import StudyPlan, StudyPlanSerializer
from src.models.study_plan_topic_model import StudyPlanTopic, StudyPlanTopicSerializer
from src.models.user_does_study_plan_and_topic_model import (
    UserDoesStudyPlanAndTopic,
    UserDoesStudyPlanAndTopicSerializer,
)
from src.models.user_follows_study_plan_model import (
    UserFollowsStudyPlan,
    UserFollowsStudyPlanSerializer,
)


def create_study_plan(data: dict, user) -> dict:
    """
    Paras:
        data (dict): dados para criação de usuário (obrigatório: title, visibility, author)

    Returns:
        dict: dados do plano criado

    Raises:
        ValidationError: se os dados forem inválidos.
    """
    # verifica se os dados sao validos
    title = data.get("title", "")

    if not re.match(r"^[\w\sÀ-ÿçÇ]+$", title):
        raise Exception(
            "Title must contain only letters (including accented), numbers, or spaces."
        )

    if len(title) > 255:
        raise Exception("Title must be 255 characters or less.")

    StudyPlanSerializer(data=data).is_valid(raise_exception=True)  # verificacao dos dados

    # cria o plano de estudos
    data["author"] = CustomUser.objects.get(id=user.id)
    visibility = data.pop("visibility", None)
    study_plan = StudyPlan.objects.create(**data)
    # visibilidade eh setada como 'private' por padrao, isso atualiza
    if visibility:
        study_plan.set_visibility(visibility)

    # usuario deve seguir o proprio plano de estudos assim que eh criado
    follow_study_plan({}, study_plan.id, user)

    study_plan.save()
    return StudyPlanSerializer(study_plan).data  # json com dados do plano


def get_execute_study_plan(user: User, study_plan_id: int) -> dict:
    """Retorna todos os planos de estudos que o usuário segue.

    Returns:
        dict: dados dos planos de estudos seguidos

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para acessar o plano
    """

    # busca o plano de estudos, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)

    # gera uma excessao se usuario nao tiver permissao para acessar o plano
    if not study_plan.access_allowed(user):
        raise PermissionDenied(
            "Você não tem permissão para acessar este plano de estudos."
        )

    # dados serializados
    result = StudyPlanSerializer(study_plan).data
    # adiciona os tópicos

    result["topics"] = []

    for topic in StudyPlanTopic.objects.filter(study_plan=study_plan):
        if UserDoesStudyPlanAndTopic.objects.filter(
            user=CustomUser.objects.get(id=user.id), study_plan_topic=topic
        ).exists():
            topic_data = StudyPlanTopicSerializer(topic).data
            topic_data["done"] = UserDoesStudyPlanAndTopic.objects.get(
                user=CustomUser.objects.get(id=user.id), study_plan_topic=topic
            ).done
            result["topics"].append(topic_data)

    return result


def check_is_author(user, study_plan):
    if user != study_plan.author.user:
        raise PermissionDenied(
            "Você não tem permissão para deletar este plano de estudos."
        )


def check_permission_plan(user: User, study_plan: StudyPlan) -> None:
    """
    Raises:
        PermissionDenied: se o usuário não tiver permissão para acessar o plano
    """
    if not study_plan.access_allowed(user):
        raise PermissionDenied(
            "Você não tem permissão para acessar este plano de estudos."
        )


def read_study_plan(study_plan_id: int, user: User) -> dict:
    """
    Returns:
        dict: dados do plano de estudos

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para acessar o plano
    """
    # busca o plano de estudos, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)

    # gera uma excessao se usuario nao tiver permissao para acessar o plano
    if not study_plan.access_allowed(user):
        raise PermissionDenied(
            "Você não tem permissão para acessar este plano de estudos."
        )

    # dados serializados
    result = StudyPlanSerializer(study_plan).data
    # adiciona os tópicos
    result["topics"] = StudyPlanTopicSerializer(
        StudyPlanTopic.objects.filter(study_plan=study_plan), many=True
    ).data
    return result


def delete_study_plan(study_plan_id: int, user: User) -> None:
    """

    Returns:
        None

    Raises:
        ObjectDoesNotExists: se o plano de estudos não for encontrado.
        PermissionDenied: se o usuário não tiver permissão para deletar o plano.
    """
    # busca o plano de estudos, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)

    # gera uma excessao se usuario nao for o autor
    check_is_author(user, study_plan)

    unfollow_study_plan({}, study_plan_id, user)

    # salva o plano de estudos como deletado
    study_plan.deleted = True
    study_plan.save()


def update_study_plan(data: dict, study_plan_id: int, user: User) -> dict:
    """

    Returns:
        dict: dados do plano de estudos atualizado

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para atualizar o plano
        ValidationError: se os dados forem inválidos
        DomainDoesNotExist: se o domínio de visibilidade não existir
    """
    # busca o plano de estudos, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)

    # gera uma excessao se usuario nao for o autor
    check_is_author(user, study_plan)

    # serializa os dados, se nao forem validos gera uma excessao
    study_plan_serializer = StudyPlanSerializer(study_plan, data=data, partial=True)
    study_plan_serializer.is_valid(raise_exception=True)

    # atualiza os dados do plano
    study_plan.title = data.get("title", study_plan.title)
    # atualiza o domínio de visibilidade, se nao existir gera uma excessao
    try:
        study_plan.set_visibility(data.get("visibility", study_plan.visibility.name))
    except ObjectDoesNotExist as e:
        raise DomainDoesNotExist(
            f"Domínio de visibilidade não encontrado: {data['visibility']}"
        )

    # salva o plano e retorna dados serializados
    study_plan.save()
    return StudyPlanSerializer(study_plan).data


def follow_study_plan(data: dict, study_plan_id: int, user: User) -> dict:
    """Adiciona um plano de estudos à lista de planos seguidos pelo usuário.

    Params:
        study_plan_id: id do plano de estudos

    Returns:
        dict: dados do plano de estudos seguido

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para seguir o plano
    """
    # busca o plano e o user, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)
    user = CustomUser.objects.get(id=user.id)

    # gera uma excessao se usuario nao tiver permissao para ver o plano
    check_permission_plan(user, study_plan)

    # adiciona o plano de estudos à lista de planos seguidos pelo usuário
    if not UserFollowsStudyPlan.objects.filter(
        user=CustomUser.objects.get(id=user.id), study_plan=study_plan
    ).exists():
        follow = UserFollowsStudyPlan.objects.create(
            user=CustomUser.objects.get(id=user.id), study_plan=study_plan
        )
        follow.save()
    else:
        follow = UserFollowsStudyPlan.objects.filter(
            user=CustomUser.objects.get(id=user.id), study_plan=study_plan
        )[0]

    # cria relacao entre o usuario e os topicos do plano
    for topic in StudyPlanTopic.objects.filter(study_plan=study_plan):
        if not UserDoesStudyPlanAndTopic.objects.filter(
            user=CustomUser.objects.get(id=user.id), study_plan_topic=topic
        ).exists():
            UserDoesStudyPlanAndTopic.objects.create(
                user=CustomUser.objects.get(id=user.id),
                study_plan_topic=topic,
            )

    # retorna os dados serializados
    return UserFollowsStudyPlanSerializer(follow).data


def get_visible_study_plans(data: dict, user: User) -> dict:
    """Retorna todos os planos de estudos visíveis.

    Returns:
        dict: dados dos planos de estudos visíveis

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para acessar o plano
    """
    study_plans = []
    for plan in StudyPlan.objects.all():
        if plan.access_allowed(user):
            study_plans.append(plan)
    return StudyPlanSerializer(study_plans, many=True).data


def unfollow_study_plan(data: dict, study_plan_id: int, user: User) -> None:
    """Remove um plano de estudos da lista de planos seguidos pelo usuário.

    Params:
        study_plan_id: id do plano de estudos

    Returns:
        None

    Raises:
        ObjectDoesNotExist: se o usuario, plano ou follow não existir
        PermissionDenied: se o usuário não tiver permissão para ver o plano
    """
    # busca o plano e o user, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)
    user = CustomUser.objects.get(id=user.id)

    # gera uma excessao se usuario nao tiver permissao para ver o plano
    if not study_plan.access_allowed(user):
        raise PermissionDenied("Você não tem permissão para ver este plano de estudos.")

    # remove o plano de estudos da lista de planos seguidos pelo usuário
    UserDoesStudyPlanAndTopic.objects.filter(
        study_plan_topic__study_plan=study_plan, user=user
    ).delete()
    UserFollowsStudyPlan.objects.filter(user=user, study_plan=study_plan).delete()


def clone_study_plan(data: dict, user: User, study_plan_id: int) -> dict:
    """Clona um plano de estudos com base nos dados passados.

    Params:
        data: dados para criação do plano de estudos
        user: usuário que está clonando o plano
        study_plan_id: id do plano de estudos a ser clonado

    Returns:
        dict: dados do plano de estudos clonado

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para clonar o plano
    """
    study_plan = StudyPlan.objects.get(id=study_plan_id)
    check_permission_plan(user, study_plan)
    new_data = StudyPlanSerializer(study_plan).data
    new_data["title"] = f"Cópia de {new_data['title']}"
    new_data["visibility"] = data.get("visibility", study_plan.visibility.name)
    new_data.pop("id")

    # cria o plano de estudos
    plan_data = create_study_plan(new_data, user)
    cloned_plan = StudyPlan.objects.get(id=plan_data["id"])

    # clona os topicos do plano
    for topic in StudyPlanTopic.objects.filter(study_plan=study_plan):
        topic_data = StudyPlanTopicSerializer(topic).data
        topic_data.pop("id")
        topic_data["study_plan"] = cloned_plan.id
        # cria clone dos topicos
        topic = StudyPlanTopic.objects.create(
            title=topic_data["title"],
            description=topic_data["description"],
            study_plan=cloned_plan,
        )

    # segue o plano de estudos
    follow_study_plan({}, cloned_plan.id, user)

    # retorna os dados do plano clonado
    return StudyPlanSerializer(cloned_plan).data
