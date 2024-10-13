from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


def login(data: dict) -> dict:
    """Verifica se o usuário existe e autentica suas credenciais, gerando um token.

    Params:
        data (dict): dados do usuário (obrigatório: username, password)

    Returns:
        dict:
        ```
        {
            "token": "secret_token_key"
        }
        ```

    Raises:
        ValidationError: se os dados forem inválidos.
    """
    serializer = AuthTokenSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    token = Token.objects.create(user=user)
    return {"token": token.key}


def logout(user: AbstractBaseUser | AnonymousUser):
    """Deleta o token do usuário.

    Params:
        user (AbstractBaseUser | AnonymousUser): usuário identificado pelo token no header

    Returns:
        None:
    """
    token = Token.objects.get(user=user)
    token.delete()
