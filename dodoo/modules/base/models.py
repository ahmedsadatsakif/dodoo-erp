from django.db import models


class BaseModel(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property
	def display_name(self):
		return self.name

	def __str__(self):
		return self.display_name

	@property
	def serialized(self, field_list=None, fetch_related=False):
		fields = self._meta.local_fields
		obj = {}
		for field in fields:
			if field_list is not None and field.name not in field_list:
				continue
			obj[field.name] = getattr(self, field.name)
		return obj

