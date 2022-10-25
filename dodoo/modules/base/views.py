import json

from django.apps import registry
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


class ViewType:
	LIST = 1
	FORM = 2
	CARD = 3
	GRAPH = 4


@require_POST
@csrf_exempt
def procedural_model_view(request: HttpRequest, module: str, model: str, function: str, view=ViewType.LIST):
	model_class = registry.apps.get_model(module, model, True)
	print(model_class)
	params = json.loads(request.body)
	print(params)
	callable_func = getattr(model_class, function)
	print(callable_func)
	return JsonResponse(callable_func(request, **params))
