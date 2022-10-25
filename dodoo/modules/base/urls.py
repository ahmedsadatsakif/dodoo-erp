from django.urls import path
from .views import procedural_model_view

urlpatterns = [
	path('<str:module>/<str:model>/<str:function>/', procedural_model_view, name='core-api-view')
]