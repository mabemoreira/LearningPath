# TODO - exclua este arquivo (apenas um exemplo)

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_data(request):
    if request.method == "GET":
        try:
            # Example GET data
            data = {"key1": "value1", "key2": "value2"}
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "POST":
        try:
            # Process POST data
            data = json.loads(request.body)
            # Example: echo the received data
            response_data = {"received": data}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
