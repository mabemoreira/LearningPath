from django.contrib.auth.models import User
from src.models.custom_user import CustomUser, CustomUserSerializer, UserSerializer


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


def read_user(id) -> dict:
    """
    Retorna os dados do usuário com o id passado.
    :param id: id do usuário
    :return: dict com os dados do usuário
    :raises: CustomUser.DoesNotExist se o usuário não existir
    """
    try:
        custom_user = CustomUser.objects.get(id=id)
        return CustomUserSerializer(custom_user).data
    except CustomUser.DoesNotExist:
        return -1


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
