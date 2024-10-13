from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from src.exceptions.response_exceptions import (
    AuthenticationFailure,
    ExceptionSerializer,
    InternalServerError,
)
from src.services.auth_service import login


class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        auth=[],
        responses={
            200: AuthTokenSerializer,
            AuthenticationFailure.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
        },
    )
    def post(self, request: Request, format=None):
        try:
            return JsonResponse(login(request.data), status=200)
        except ValidationError as e:
            return AuthenticationFailure()
        except Exception as e:
            return InternalServerError()
