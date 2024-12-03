from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from src.models.custom_user_model import CustomUser, CustomUserSerializer, UserSerializer


def create_custom_user(data: dict) -> dict:
    """
    Params:
        data (dict): dados para criação de usuário (obrigatório: username, password)

    Returns:
        dict: dados do usuário criado

    Raises:
        ValidationError: se os dados forem inválidos.
    """
    password = data.get("password")
    if not password or len(password) < 8 or len(password) > 128:
        raise ValidationError("Password must be between 8 and 128 characters.")
    UserSerializer(data=data).is_valid(raise_exception=True)  # verificacao dos dados
    user = User.objects.create_user(**data)  # cria o usuario na tabela do Django
    custom_user = CustomUser.objects.create(user=user)  # cria o CustomUser
    custom_user.save()  # salva no BD
    return CustomUserSerializer(custom_user).data


def read_custom_user(user_id) -> dict:
    """
    Returns:
        dict: dados do usuário

    Raises:
        ObjectDoesNotExist: se o usuário não existir
        ValueError: se o id for inválido
    """
    custom_user = CustomUser.objects.get(id=user_id)
    return CustomUserSerializer(custom_user).data


def check_permission_user(user: User, requesting_user: User) -> None:
    """
    Raises:
        PermissionDenied: se o usuário não tiver permissão para acessar o usuário
    """
    if not requesting_user.is_superuser and requesting_user.id != user.id:
        raise PermissionDenied("Você não tem permissão para acessar este usuário.")


def delete_custom_user(user_id: int, requesting_user: User) -> None:
    """

    Params:
        user_id (int)
        requesting_user (User): usuário que está fazendo a solicitação

    Returns:
        None

    Raises:
        ObjectDoesNotExists: se o usuário não for encontrado.
        PermissionDenied: se o usuário não tiver permissão para deletar.
    """
    user = User.objects.get(id=user_id)
    check_permission_user(user, requesting_user)
    user.delete()


def update_custom_user(data: dict, user_id: int, requesting_user: User) -> dict:
    """
    Params:
        user_id: id do usuário
        requesting_user (User): usuário que está fazendo a solicitação

    Returns:
        dict: dados do usuário atualizado

    Raises:
        ObjectDoesNotExist: se o usuário não existir
        ValueError: se o id for inválido
        PermissionDenied: se o usuário não tiver permissão para atualizar.
        ValidationError: se os dados forem inválidos.
    """
    user = User.objects.get(id=user_id)
    check_permission_user(user, requesting_user)
    user_serializer = UserSerializer(user, data=data, partial=True)
    user_serializer.is_valid(raise_exception=True)
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.save()
    custom_user = CustomUser.objects.get(user=user)
    return CustomUserSerializer(custom_user).data
