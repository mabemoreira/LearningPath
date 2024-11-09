from django.contrib.auth.models import User
from src.models.custom_user_model import CustomUser, CustomUserSerializer, UserSerializer
from src.models.study_plan_model import StudyPlan, StudyPlanSerializer
from src.models.study_plan_topic_model import StudyPlanTopic, StudyPlanTopicSerializer


def create_study_plan(data: dict) -> dict:
    """Cria um StudyPlan com base nos dados passados.

    Params:
        data (dict): dados para criação de usuário (obrigatório: title, visibility, author)

    Returns:
        dict: dados do plano criado

    Raises:
        ValidationError: se os dados forem inválidos.
    """
    StudyPlanSerializer(data=data).is_valid(raise_exception=True)  # verificacao dos dados
    study_plan = StudyPlan.objects.create(**data)  # cria o usuario na tabela do Django
    study_plan.save()  # salva no BD
    return StudyPlanSerializer(study_plan).data


def read_study_plan(study_plan_id) -> dict:
    """Retorna os dados do plano de estudos com o id passado.
    Params:
        user_id: id do plano de estudos

    Returns:
        dict: dados do plano de estudos

    Raises:
        ObjectDoesNotExist: se o plano de estudos não existir
        ValueError: se o id for inválido
    """
    study_plan = StudyPlan.objects.get(id=study_plan_id)
    topics = StudyPlanTopic.objects.filter(study_plan=study_plan)
    return StudyPlanSerializer(study_plan).data


def delete_custom_user(user_id: int) -> None:
    """Deleta um usuário através do id.

    Params:
        user_id (int)

    Returns:
        None

    Raises:
        ObjectDoesNotExists: se o usuário não for encontrado.
    """
    user = User.objects.get(id=user_id)
    user.delete()


def update_custom_user(data: dict, user_id: int) -> dict:
    """Atualiza os dados do usuário com o id passado.

    Params:
        user_id: id do usuário

    Returns:
        dict: dados do usuário atualizado

    Raises:
        ObjectDoesNotExist: se o usuário não existir
        ValueError: se o id for inválido
    """
    user = User.objects.get(id=user_id)
    user_serializer = UserSerializer(user, data=data, partial=True)
    user_serializer.is_valid(raise_exception=True)
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.save()
    custom_user = CustomUser.objects.get(user=user)
    return CustomUserSerializer(custom_user).data
