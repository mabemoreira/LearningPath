import json

from django.forms import ValidationError
from django.http import JsonResponse
from django.views import View
from src.services.custom_user_service import create_custom_user, read_user


class UserController(View):
    def get(self, request):
        try:
            retorno = read_user(int(request.body))
            if retorno == -1:
                return JsonResponse({"error": "User not found"}, status=404)
            return JsonResponse(retorno, status=200)
        except ValidationError as e:
            return JsonResponse({"error": e.message}, status=500)

    def post(self, request):
        try:
            return JsonResponse(
                create_custom_user(json.loads(request.body)), status=200
            )
        except ValidationError as e:
            return JsonResponse({"error": e.message}, status=500)

    def delete(self, request):
        pass

    def put(self, request):
        pass
