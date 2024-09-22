import json

from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.http import HttpRequest, JsonResponse
from django.views import View
from src.exceptions.response_exceptions import (
    EntityNotFound,
    InternalServerError,
    UnprocessableEntity,
)
from src.services.custom_user_service import create_custom_user, delete_custom_user


class UserController(View):
    def get(self, request: HttpRequest, user_id: int):
        try:
            pass
        except Exception as e:
            return InternalServerError()

    def post(self, request: HttpRequest):
        try:
            return JsonResponse(create_custom_user(json.loads(request.body)), status=200)
        except ValidationError as e:
            return UnprocessableEntity()
        except Exception as e:
            return InternalServerError()

    def delete(self, request: HttpRequest, user_id: int):
        try:
            delete_custom_user(user_id)
            return JsonResponse({}, status=204)
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except Exception as e:
            return InternalServerError()

    def put(self, request: HttpRequest):
        try:
            pass
        except Exception as e:
            return InternalServerError()
