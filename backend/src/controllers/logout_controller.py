from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from src.exceptions.response_exceptions import (
    EntityNotFound,
    ExceptionSerializer,
    InternalServerError,
)
from src.services.auth_service import logout


class LogoutView(APIView):

    @extend_schema(
        responses={
            204: None,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
        },
    )
    def post(self, request: HttpRequest, format=None):
        try:
            logout(request.user)
            return JsonResponse({}, status=204)
        except ObjectDoesNotExist:
            return EntityNotFound()
        except Exception:
            return InternalServerError()
