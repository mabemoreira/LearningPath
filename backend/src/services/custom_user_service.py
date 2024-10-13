from django.contrib.auth.models import User
from src.models.custom_user_model import CustomUser, CustomUserSerializer, UserSerializer


def create_custom_user(data: dict) -> dict:
    """Cria um CustomUser com base nos dados passados.

    Params:
        data (dict): dados para criação de usuário (obrigatório: username, password)

    Returns:
        dict: dados do usuário criado

    Raises:
        ValidationError: se os dados forem inválidos.
    """
    UserSerializer(data=data).is_valid(raise_exception=True)  # verificacao dos dados
    user = User.objects.create_user(**data)  # cria o usuario na tabela do Django
    custom_user = CustomUser.objects.create(user=user)  # cria o CustomUser
    custom_user.save()  # salva no BD
    return CustomUserSerializer(custom_user).data


def read_custom_user(user_id) -> dict:
    """Retorna os dados do usuário com o id passado.
    Params:
        user_id: id do usuário

    Returns:
        dict: dados do usuário

    Raises:
        ObjectDoesNotExist: se o usuário não existir
        ValueError: se o id for inválido
    """
    custom_user = CustomUser.objects.get(id=user_id)
    return CustomUserSerializer(custom_user).data


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
