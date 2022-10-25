import binascii
import uuid
from datetime import date, datetime, time

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


def parse_fk(model, val):
	if isinstance(val, dict):
		created = deserialize_json(model, val, True)
		created.save()
		return created
	else:
		try:
			return model.objects.get(pk=val)
		except ObjectDoesNotExist:
			return None


def parse_m2m(model, vals):
	out = []
	for val in vals:
		if isinstance(val, dict):
			instance = deserialize_json(model, val, True)
			instance.save()
			out.append(instance)
		else:
			try:
				inst = model.objects.get(pk=val)
				out.append(inst)
			except ObjectDoesNotExist:
				inst = None
	return out


def json_serialize_related_field(field, value, recursive):
	if isinstance(field, models.ForeignKey):
		if recursive is True:
			val = json_serialize_model(value, recursive)
			return val
		else:
			return value.pk
	elif isinstance(field, models.ManyToManyField):
		if recursive is True:
			ret = []
			for item in value.all():
				ret.append(json_serialize_model(item, recursive))
			return ret
		else:
			print(value.all())
			return value.str()


def json_serialize_field(field, value, recursive):
	if isinstance(field, (models.ForeignKey, models.ManyToManyField)):
		return json_serialize_related_field(field, value, recursive)
	elif isinstance(field, (models.DateField, models.TimeField, models.DateTimeField)):
		return value.isoformat()
	elif isinstance(field, (models.FileField, models.ImageField)):
		if value._file is not None:
			return value.path
		return None
	elif isinstance(field, (models.UUIDField)):
		return value.hex
	elif isinstance(field, models.BinaryField):
		return binascii.hexlify(value)
	elif isinstance(field, models.DecimalField):
		return float(value)
	else:
		return value


def json_serialize_model(model_instance, recursive=False):
	if model_instance is None:
		return None
	local_fields = model_instance._meta.local_fields
	response = {}
	for field in local_fields:
		response[field.name] = json_serialize_field(field, getattr(model_instance, field.name), recursive)

	if recursive is False:
		return response

	related_fields = model_instance._meta.local_many_to_many
	for related in related_fields:
		response[related.name] = json_serialize_field(related, getattr(model_instance, related.name), recursive)

	return response


def native_data_type(field, val):
	if isinstance(field, models.ForeignKey):
		return parse_fk(field.related_model, val)
	elif isinstance(field, models.ManyToManyField):
		return parse_m2m(field.related_model, val)
	elif isinstance(field, models.DateTimeField):
		return datetime.fromisoformat(val)
	elif isinstance(field, models.DateField):
		return date.fromisoformat(val)
	elif isinstance(field, models.TimeField):
		return time.fromisoformat(val)
	elif isinstance(field, models.UUIDField):
		return uuid.UUID(val)
	elif isinstance(field, models.DecimalField):
		return float(val)
	elif isinstance(field, models.BinaryField):
		return binascii.unhexlify(val)
	elif isinstance(field, (models.FileField, models.ImageField)):
		if val._file is not None:
			return val.path
		return None
	else:
		return val


def deserialize_json(model_class, data, recursive=False):
	instance = model_class()
	local_fields = model_class._meta.local_fields
	for field in local_fields:
		val = data.get(field.name, None)
		if val is not None:
			setattr(instance, field.name, native_data_type(field, val))
	if recursive is False:
		return instance

	instance.save()
	related_fields = model_class._meta.local_many_to_many
	for rel_field in related_fields:
		val = data.get(rel_field.name, [])
		m2m = getattr(instance, rel_field.name)
		m2m.set(native_data_type(rel_field, val))

	return instance


def get_field_type(field):
	if isinstance(field, (models.TimeField, models.DateTimeField, models.DateField)):
		return 'datetime'
	elif isinstance(field, (models.FileField, models.ImageField)):
		return 'file'
	elif isinstance(field, (models.IntegerField, models.BigIntegerField, models.SmallIntegerField, models.PositiveIntegerField, models.PositiveSmallIntegerField, models.PositiveBigIntegerField, models.DecimalField, models.FloatField)):
		return 'number'
	elif isinstance(field, (models.BooleanField, models.NullBooleanField)):
		return 'checkbox'
	elif isinstance(field, (models.EmailField)):
		return 'email'
	elif isinstance(field, (models.OneToOneField, models.ForeignKey)):
		return 'select'
	elif isinstance(field, (models.ManyToManyField)):
		return 'multi-select'
	else:
		return 'text'


def get_model_schema(model_class, recursive=False):
	local_fields = model_class._meta.local_fields
	schema = {}
	for field in local_fields:
		field_dict = field.__dict__
		print(field_dict)
		schema[field.name] = {
			'name': field_dict.get('name', None),
			'label': field_dict.get('verbose_name', None),
			'type': get_field_type(field),
			'required': field_dict.get('blank', True) is False,
			'unique': field_dict.get('_unique', field_dict.get('primary_key', False)),
			'max_length': field_dict.get('max_length', None),
		}
	return schema


class RestModel(models.Model):
	class Meta:
		abstract = True

	def _serialized(self, recursive=False):
		return json_serialize_model(self, recursive)

	@classmethod
	def schema(cls, data):
		return get_model_schema(cls)

	@classmethod
	def new(cls, data):
		instance = deserialize_json(cls, data, recursive=True)
		instance.save()
		return instance._serialized()

	@classmethod
	def list(cls, data):
		start = data.get('start', 0)
		limit = data.get('limit', 100)
		recursive = data.get('related', False)
		items = cls.objects.all()[start:start+limit]
		ret = []
		for item in items:
			ret.append(json_serialize_model(item, recursive))
		return ret

	@classmethod
	def get(cls, data):
		pk = data.get('id', None)
		if pk is None:
			return None

		instance = cls.objects.get(pk=pk)

		return json_serialize_model(instance)

	@classmethod
	def update(cls, data):
		pass

	@classmethod
	def remove(cls, data):
		pass
