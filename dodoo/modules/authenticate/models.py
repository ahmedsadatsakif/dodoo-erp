import uuid
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import dispatcher
from django.contrib.auth import authenticate
import django.contrib.auth.models as auth_models


@dispatcher.receiver(models.signals.post_save)
def assign_user_account(signal, sender, instance, **kwargs):
	if sender == auth_models.User:
		is_created = kwargs.get('created', False)
		if is_created is True:
			account = Account(user=instance, api=ApiToken.get_default())
			account.save()


class ApiToken(models.Model):
	application_name = models.CharField(max_length=127)
	application_id = models.SlugField(max_length=127, unique=True)
	token = models.CharField(max_length=127, unique=True)

	def __str__(self):
		return self.application_name

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.token = uuid.uuid5(uuid.NAMESPACE_OID, self.application_id).hex
		return super(ApiToken, self).save(force_insert, force_update, using, update_fields)

	@staticmethod
	def get_default():
		try:
			default_inst = ApiToken.objects.get(application_id='default')
			return default_inst
		except ObjectDoesNotExist as dne:
			default_inst = ApiToken(application_id='default', application_name='Root')
			default_inst.save()
			return default_inst


class Account(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accounts', on_delete=models.CASCADE)
	api = models.ForeignKey(ApiToken, related_name='accounts', null=True, blank=False, on_delete=models.CASCADE)
	session_token = models.CharField(max_length=127, db_index=True)
	valid_until = models.DateTimeField()

	def __str__(self):
		return '(%s) %s' % (self.api, self.user)

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.valid_until = datetime.now() + timedelta(hours=2)
		return super(Account, self).save(force_insert, force_update, using, update_fields)

	@staticmethod
	def login(params):
		username = params.get('email', None)
		password = params.get('password', None)
		user = authenticate(username=username, password=password)
		if user is not None:
			user_account = Account.objects.get(user=user)
			user_account.session_token = uuid.uuid5(uuid.NAMESPACE_OID, '%s%s' % (user_account.api.token, getattr(user_account.user, auth_models.User.USERNAME_FIELD))).hex
			return Account.serialized_session_data(user_account)
		return None

	@staticmethod
	def serialized_session_data(user_account):
		inst = user_account
		filtered = dict(
			session_token=inst.session_token,
			validity=timedelta(hours=2).seconds,
			user=dict(username=inst.user.username, email=inst.user.email)
		)
		inst.save()
		jwt_val = jwt.encode(filtered, inst.api.application_id, algorithm='HS512')
		return jwt_val

	@staticmethod
	def validate(params, files, headers):
		auth_header = headers.get('HTTP_AUTHORIZATION', None)
		if auth_header is not None:
			bearer, token = auth_header.split(' ', 1)
			try:
				acc = Account.objects.get(session_token=token, valid_until__gt=datetime.now())
			except ObjectDoesNotExist:
				acc = None
			if bearer == 'Bearer' and acc is not None:
				return Account.serialized_session_data(acc)