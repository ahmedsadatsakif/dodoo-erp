from django.db import models as m
from ..base.models import BaseModel


class Country(BaseModel):
	requires_state = m.BooleanField(default=False)
	requires_zip = m.BooleanField(default=False)
	requires_city = m.BooleanField(default=False)


class State(BaseModel):
	country = m.ForeignKey(Country, on_delete=m.CASCADE)


class City(BaseModel):
	state = m.ForeignKey(State, on_delete=m.CASCADE)


class AddressMixin(m.Model):
	class Meta:
		abstract = True

	street_1 = m.CharField(max_length=255)
	street_2 = m.CharField(max_length=255, null=True, blank=True)
	city = m.ForeignKey(City, on_delete=m.SET_NULL, null=True, blank=True)
	state = m.ForeignKey(State, on_delete=m.SET_NULL, null=True, blank=True)
	zip = m.CharField(max_length=63, null=True, blank=True)
	country = m.ForeignKey(Country, on_delete=m.SET_NULL, null=True, blank=True)

	@property
	def formatted_address(self):
		address = '%s\n%s\n,%s,%s,%s\n%s' % (self.street_1, self.street_2, self.city.name, self.state.name, self.zip, self.country.name)
		address = self.street_1
		address += (',\n%s' % self.street_2) if self.street_2 is not None else ''
		address += (',\n%s' % self.city.name) if self.city is not None else ''
		address += (',%s' % self.state.name) if self.state is not None else ''
		address += (',%s' % self.country.name) if self.country is not None else ''
		address += ('\n%s' % self.zip) if self.zip is not None else ''
		return address


class Currency(BaseModel):
	symbol = m.CharField(max_length=7)
	code = m.CharField(max_length=15)
	country = m.ForeignKey(Country, on_delete=m.CASCADE)


class Entity(BaseModel, AddressMixin):
	type = m.IntegerField(choices=[
		(1, 'Individual'),
		(2, 'Company')
	])
	logo = m.ImageField(upload_to='company/')
	grouped_under = m.ForeignKey('self', on_delete=m.CASCADE)


class EntityRelation(BaseModel):
	relation = m.IntegerField(choices=[
		(1, 'Customer'),
		(2, 'Vendor'),
		(3, 'Employee'),
		(4, 'Lead')
	])
	entity = m.ForeignKey(Entity, on_delete=m.CASCADE)


class Bank(BaseModel):
	entity = m.ForeignKey(Entity, on_delete=m.CASCADE)
	pass


class Account(BaseModel):
	type = m.IntegerField(choices=[
		(1, 'Bank'),
		(2, 'Cash')
	])
	bank = m.ForeignKey(Bank, on_delete=m.CASCADE)
	number = m.CharField(max_length=63)
	reference = m.CharField(max_length=511)
	credit = m.FloatField()
	debit = m.FloatField()

	@property
	def balance(self):
		return self.debit.to_python() - self.credit.to_python()


class CompanyType(BaseModel):
	pass


class Company(BaseModel):
	type = m.ManyToManyField(CompanyType)
	entity = m.ForeignKey(Entity, on_delete=m.CASCADE)
	partners = m.ManyToManyField(Entity)
	accounts = m.ManyToManyField(Account)