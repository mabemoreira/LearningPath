from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.views import APIView
from src.exceptions.business_rules_exceptions import DomainDoesNotExist
from src.exceptions.response_exceptions import (
    EntityNotFound,
    ExceptionSerializer,
    InternalServerError,
    UnauthorizedAccess,
    UnprocessableEntity,
)
from src.models.study_plan_model import StudyPlan, StudyPlanSerializer
from src.services.study_plan_service import (
    clone_study_plan,
    create_study_plan,
    delete_study_plan,
    follow_study_plan,
    get_execute_study_plan,
    get_visible_study_plans,
    read_study_plan,
    unfollow_study_plan,
    update_study_plan,
)


class StudyPlanController(APIView):

    @extend_schema(
        responses={
            200: StudyPlanSerializer,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
            UnauthorizedAccess.status_code: ExceptionSerializer,
        },
    )
    def get(self, request: Request, study_plan_id: int = -1):
        try:
            if study_plan_id > 0:
                if "execute" in request.path:
                    return JsonResponse(
                        get_execute_study_plan(request.user, study_plan_id), status=200
                    )
                else:
                    study_plan = read_study_plan(study_plan_id, request.user)
                    return JsonResponse(study_plan, status=200)
            elif "get_all" in request.path:
                return self.get_all(request)
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except PermissionDenied as e:
            return UnauthorizedAccess()
        except Exception as e:
            return InternalServerError()

    @extend_schema(
        request=StudyPlanSerializer,
        responses={
            200: StudyPlanSerializer,
            UnprocessableEntity.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
            EntityNotFound.status_code: ExceptionSerializer,
            UnauthorizedAccess.status_code: ExceptionSerializer,
        },
    )
    def post(self, request: Request, study_plan_id: int = None):
        if study_plan_id:
            if "clone" in request.path:
                return self.post_clone(request, study_plan_id)
            elif "follow" in request.path:
                return self.post_follow(request, study_plan_id)
            else:
                return JsonResponse({"detail": "Ação não permitida"}, status=400)
        return self.post_create(request)

    def post_clone(self, request: Request, study_plan_id: int):
        try:
            return JsonResponse(
                clone_study_plan(request.data, request.user, study_plan_id), status=200
            )
        except PermissionDenied as e:
            return UnauthorizedAccess()
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except Exception as e:
            return InternalServerError()

    def post_follow(self, request: Request, study_plan_id: int):
        try:
            return JsonResponse(
                follow_study_plan(dict(), study_plan_id, request.user), status=200
            )
        except PermissionDenied as e:
            return UnauthorizedAccess()
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except Exception as e:
            return InternalServerError()

    def get_all(self, request: Request):
        try:
            visible_study_plans = get_visible_study_plans({}, request.user)
            return JsonResponse(visible_study_plans, safe=False, status=200)
        except Exception as e:
            return InternalServerError()

    def post_create(self, request: Request):
        try:
            return JsonResponse(create_study_plan(request.data, request.user), status=200)
        except ValidationError as e:
            return UnprocessableEntity()
        except Exception as e:
            return InternalServerError()

    @extend_schema(
        request=StudyPlanSerializer,
        responses={
            204: None,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
            UnauthorizedAccess.status_code: ExceptionSerializer,
        },
    )
    def delete(self, request: Request, study_plan_id: int):
        if "follow" in request.path:
            return self.unfollow_plan(request, study_plan_id)
        return self.delete_plan(request, study_plan_id)

    def delete_plan(self, request: Request, study_plan_id: int):
        try:
            delete_study_plan(study_plan_id, request.user)
            return JsonResponse({}, status=204)
        except ObjectDoesNotExist:
            return EntityNotFound()
        except PermissionDenied:
            return UnauthorizedAccess()
        except Exception as e:
            return InternalServerError()

    def unfollow_plan(self, request: Request, study_plan_id: int):
        try:
            unfollow_study_plan("", study_plan_id, request.user)
            return JsonResponse({}, status=204)
        except ObjectDoesNotExist:
            return EntityNotFound()
        except PermissionDenied:
            return UnauthorizedAccess()
        except Exception as e:
            return InternalServerError()

    @extend_schema(
        request=StudyPlanSerializer,
        responses={
            200: StudyPlanSerializer,
            UnprocessableEntity.status_code: ExceptionSerializer,
            EntityNotFound.status_code: ExceptionSerializer,
            InternalServerError.status_code: ExceptionSerializer,
            UnauthorizedAccess.status_code: ExceptionSerializer,
        },
    )
    def put(self, request: Request, study_plan_id: int):
        try:
            data = request.data
            user = request.user
            return JsonResponse(update_study_plan(data, study_plan_id, user), status=200)
        except ObjectDoesNotExist as e:
            return EntityNotFound()
        except PermissionDenied as e:
            return UnauthorizedAccess()
        except ValidationError as e:
            return UnprocessableEntity()
        except DomainDoesNotExist as e:
            return UnprocessableEntity(e.details)
        except Exception as e:
            return InternalServerError()
