from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.views import APIView
from src.exceptions.response_exceptions import (
    EntityNotFound,
    ExceptionSerializer,
    InternalServerError,
    UnauthorizedAccess,
    UnprocessableEntity,
)
from src.models.custom_user_model import CustomUserSerializer, UserSerializer
from src.services.custom_user_service import (
    create_custom_user,
    delete_custom_user,
    read_custom_user,
    update_custom_user,
)


class UserController(APIView):
    def get_permissions(self):
        permissions = super().get_permissions()

        # Only post method should allow unauthenticated requests
        if self.request.method.lower() == "post":
            return []
        return permissions

    @extend_schema(
        responses={
            200: CustomUserSerializer,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
        },
    )
    def get(self, request: Request, user_id: int):
        if user_id == 0:
            user_id = request.user.id
        try:
            user = read_custom_user(user_id)
            return JsonResponse(user, status=200)
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except Exception as e:
            return InternalServerError()

    @extend_schema(
        auth=[],
        request=UserSerializer,
        responses={
            200: CustomUserSerializer,
            UnprocessableEntity.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
        },
    )
    def post(self, request: Request):
        try:
            return JsonResponse(create_custom_user(request.data), status=200)
        except ValidationError as e:
            return UnprocessableEntity()
        except Exception as e:
            return InternalServerError()

    @extend_schema(
        request=UserSerializer,
        responses={
            204: None,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
            UnauthorizedAccess.status_code: ExceptionSerializer,
        },
    )
    def delete(self, request: Request, user_id: int):
        try:
            delete_custom_user(user_id, request.user)
            return JsonResponse({}, status=204)
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except PermissionDenied as e:
            return UnauthorizedAccess()
        except Exception as e:
            return InternalServerError()

    @extend_schema(
        request=UserSerializer,
        responses={
            200: CustomUserSerializer,
            UnprocessableEntity.status_code: ExceptionSerializer,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
            UnauthorizedAccess.status_code: ExceptionSerializer,
        },
    )
    def put(self, request: Request, user_id: int):
        try:
            data = request.data
            return JsonResponse(
                update_custom_user(data, user_id, request.user), status=200
            )
        except ValidationError as e:
            return UnprocessableEntity()
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except PermissionDenied as e:
            return UnauthorizedAccess()
        except Exception as e:
            return InternalServerError()
