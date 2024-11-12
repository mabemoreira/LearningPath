from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from src.exceptions.business_rules_exceptions import DomainDoesNotExist
from src.models.custom_user_model import CustomUser
from src.models.domain_model import Domain
from src.models.study_plan_model import StudyPlan, StudyPlanSerializer
from src.models.study_plan_topic_model import StudyPlanTopic, StudyPlanTopicSerializer


def create_study_plan(data: dict, user) -> dict:
    """Cria um StudyPlan com base nos dados passados.

    Params:
        data (dict): dados para criação de usuário (obrigatório: title, visibility, author)

    Returns:
        dict: dados do plano criado

    Raises:
        ValidationError: se os dados forem inválidos.
    """
    # verifica se os dados sao validos
    StudyPlanSerializer(data=data).is_valid(raise_exception=True)  # verificacao dos dados

    # cria o plano de estudos
    data["author"] = CustomUser.objects.get(id=user.id)
    visibility = data.pop("visibility", None)
    study_plan = StudyPlan.objects.create(**data)
    if visibility:
        study_plan.set_visibility(visibility)

    # salva e retorna os dados serializados
    study_plan.save()
    return StudyPlanSerializer(study_plan).data


def read_study_plan(study_plan_id: int, user: User) -> dict:
    """Retorna os dados do plano de estudos com o id passado.
    Params:
        study_plan_id: id do plano de estudos

    Returns:
        dict: dados do plano de estudos

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        PermissionDenied: se o usuário não tiver permissão para acessar o plano
    """
    # busca o plano de estudos, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)

    # gera uma excessao se usuario nao tiver permissao para acessar o plano
    # TODO: permitir get se o usuário seguir o plano de estudos
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
    """Deleta um plano de estudos através do id.

    Params:
        study_plan_id (int)

    Returns:
        None

    Raises:
        ObjectDoesNotExists: se o plano de estudos não for encontrado.
        PermissionDenied: se o usuário não tiver permissão para deletar o plano.
    """
    # busca o plano de estudos, se nao existir gera uma excessao
    study_plan = StudyPlan.objects.get(id=study_plan_id)

    # gera uma excessao se usuario nao for o autor
    if not user == study_plan.author.user:
        raise PermissionDenied(
            "Você não tem permissão para deletar este plano de estudos."
        )

    # salva o plano de estudos como deletado
    study_plan.deleted = True
    study_plan.save()


def update_study_plan(data: dict, study_plan_id: int, user: User) -> dict:
    """Atualiza os dados do plano de estudos com o id passado.

    Params:
        study_plan_id: id do plano de estudos

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
    if not user == study_plan.author.user:
        raise PermissionDenied(
            "Você não tem permissão para atualizar este plano de estudos."
        )

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
            f"Domínio de visibilidade não encontrado: {data["visibility"]}"
        )

    # salva o plano e retorna dados serializados
    study_plan.save()
    return StudyPlanSerializer(study_plan).data
