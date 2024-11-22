from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.views import APIView
from src.exceptions.response_exceptions import (
    EntityNotFound,
    ExceptionSerializer,
    InternalServerError,
)
from src.models.domain_model import DomainSerializer
from src.services.domain_service import read_domain


class DomainController(APIView):

    @extend_schema(
        responses={
            200: DomainSerializer,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
        },
    )
    def get(self, request: Request, domain_id: int):
        try:
            domain = read_domain(domain_id)
            return JsonResponse(domain, status=200)
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except Exception as e:
            return InternalServerError()
