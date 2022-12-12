from django.core.exceptions import ObjectDoesNotExist
from django.db import models as m
from ..base.models import BaseModel


class AccountableItem(m.Model):
	pass


class Accountable(m.Model):
	class Meta:
		abstract = True

	transaction_type = m.IntegerField(choices=[
		(1, 'Assets'),
		(2, 'Liabilities'),
	])
	credit = m.FloatField()
	debit = m.FloatField()
	balance = m.FloatField()


class JournalEntry(BaseModel, Accountable):
	item = m.ForeignKey(AccountableItem, on_delete=m.SET_NULL)


class Journal(BaseModel):
	entries = m.ManyToManyField(JournalEntry)

