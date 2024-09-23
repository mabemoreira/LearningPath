from django.http import JsonResponse


class Unauthorized(JsonResponse):
    def __init__(self, details: str = None):
        if details is None:
            details = "Usuário sem autenticação!"

        super().__init__({"details": details}, status=401)


class EntityNotFound(JsonResponse):
    def __init__(self, details: str = None):
        if details is None:
            details = "A entidade não foi encontrada!"

        super().__init__({"details": details}, status=404)


class UnprocessableEntity(JsonResponse):
    def __init__(self, details: str = None):
        if details is None:
            details = "Alguma regra de negócio foi infringida!"

        super().__init__({"details": details}, status=422)


class InternalServerError(JsonResponse):
    def __init__(self, details: str = None):
        if details is None:
            details = "Ocorreu algum erro de execução no servidor!"

        super().__init__({"details": details}, status=500)


class NotImplemented(JsonResponse):
    def __init__(self, details: str = None):
        if details is None:
            details = "O método requisitado ainda não foi implementado!"

        super().__init__({"details": details}, status=501)
