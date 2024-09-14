from django.contrib.auth.models import User
from src.models.custom_user import (
    CustomUser,
    CustomUserSerializer,
    UserSerializer,
)


def create_custom_user(data: dict) -> dict:
    """
    Cria um CustomUser com base nos dados passados.
    :param data: dict com os dados do usuário (obrigatorio: username, password)
    :return: dict com os dados do usuário
    :raises: ValidationError se os dados forem inválidos
    """
    UserSerializer(data=data).is_valid(
        raise_exception=True
    )  # verificacao dos dados
    user = User.objects.create_user(
        **data
    )  # cria o usuario na tabela do Django
    custom_user = CustomUser.objects.create(user=user)  # cria o CustomUser
    custom_user.save()  # salva no BD
    return CustomUserSerializer(custom_user).data
