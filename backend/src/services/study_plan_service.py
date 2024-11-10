from django.core.exceptions import ObjectDoesNotExist
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
    data["author"] = CustomUser.objects.get(id=user.id)
    StudyPlanSerializer(data=data).is_valid(raise_exception=True)  # verificacao dos dados
    study_plan = StudyPlan.objects.create(**data)
    study_plan.save()  # salva no BD
    return StudyPlanSerializer(study_plan).data


def read_study_plan(study_plan_id) -> dict:
    """Retorna os dados do plano de estudos com o id passado.
    Params:
        study_plan_id: id do plano de estudos

    Returns:
        dict: dados do plano de estudos

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        ValueError: se o id for inválido
    """
    study_plan = StudyPlan.objects.get(id=study_plan_id)
    result = StudyPlanSerializer(study_plan).data
    result["topics"] = StudyPlanTopicSerializer(
        StudyPlanTopic.objects.filter(study_plan=study_plan), many=True
    ).data
    return StudyPlanSerializer(study_plan).data


def delete_study_plan(study_plan_id: int) -> None:
    """Deleta um plano de estudos através do id.

    Params:
        study_plan_id (int)

    Returns:
        None

    Raises:
        ObjectDoesNotExists: se o plano de estudos não for encontrado.
    """
    study_plan = StudyPlan.objects.get(id=study_plan_id)
    study_plan.deleted = True
    study_plan.save()


def update_study_plan(data: dict, study_plan_id: int) -> dict:
    """Atualiza os dados do plano de estudos com o id passado.

    Params:
        study_plan_id: id do plano de estudos

    Returns:
        dict: dados do plano de estudos atualizado

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        ValueError: se o id for inválido

    """
    study_plan = StudyPlan.objects.get(id=study_plan_id)
    study_plan_serializer = StudyPlanSerializer(study_plan, data=data, partial=True)
    study_plan_serializer.is_valid(raise_exception=True)
    study_plan.title = data.get("title", study_plan.title)
    try:
        study_plan.visibility = Domain.objects.get(
            name=data["visibility"], type="visibility", relationship="StudyPlan"
        )
    except ObjectDoesNotExist:
        raise DomainDoesNotExist(f"Visibility domain not found: {data["visibility"]}")
    study_plan.deleted = data.get("deleted", study_plan.deleted)
    study_plan.save()
    return StudyPlanSerializer(study_plan).data
