from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered


def load_all_models():
	models = apps.get_models()
	for model in models:
		try:
			admin.site.register(model)
		except AlreadyRegistered:
			pass

load_all_models()
