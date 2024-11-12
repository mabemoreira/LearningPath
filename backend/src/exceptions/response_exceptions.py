from django.http import JsonResponse
from rest_framework import serializers


class ExceptionSerializer(serializers.Serializer):
    details = serializers.CharField()


class AuthenticationFailure(JsonResponse):
    status_code = 401

    def __init__(self, details: str = None):
        if details is None:
            details = "Falha na autenticação!"

        super().__init__({"details": details})


class EntityNotFound(JsonResponse):
    status_code = 404

    def __init__(self, details: str = None):
        if details is None:
            details = "A entidade não foi encontrada!"

        super().__init__({"details": details})


class UnauthorizedAccess(JsonResponse):
    status_code = 403

    def __init__(self, details: str = None):
        if details is None:
            details = "Acesso não autorizado!"

        super().__init__({"details": details})


class UnprocessableEntity(JsonResponse):
    status_code = 422

    def __init__(self, details: str = None):
        if details is None:
            details = "Alguma regra de negócio foi infringida!"

        super().__init__({"details": details})


class InternalServerError(JsonResponse):
    status_code = 500

    def __init__(self, details: str = None):
        if details is None:
            details = "Ocorreu algum erro de execução no servidor!"

        super().__init__({"details": details})


class NotImplemented(JsonResponse):
    status_code = 501

    def __init__(self, details: str = None):
        if details is None:
            details = "O método requisitado ainda não foi implementado!"

        super().__init__({"details": details})
