from django.db import models as m
from ..base.models import BaseModel


class Specialization(BaseModel):
	pass


class Degree(BaseModel):
	pass


class Doctor(BaseModel):
	public_methods = [
		{
			'name': 'get_schedule',
			'label': 'Get Schedule'
		},
		{
			'name': 'search_doctor',
			'label': 'Search Doctor'
		}
	]

	title = m.CharField(max_length=31)
	profile_image = m.ImageField(upload_to='doctor/profile')
	specializations = m.ManyToManyField(Specialization)
	degrees = m.ManyToManyField(Degree)

	@classmethod
	def search_doctor(cls, name=None, degree=None, specialization=None):
		search_params = {}

		if name is not None:
			search_params.update(dict(name=name))
		if degree is not None:
			search_params.update(dict(degrees__in=degree))
		if specialization is not None:
			search_params.update(dict(specializations__in=specialization))
		doctors = Doctor.objects.filter(**search_params)
		out = []
		for doc in doctors:
			out.append(doc._serialize(recursive=True))
		return out

	def get_schedule(self):
		scheduled_slots = self.schedule_set.all()
		out = []
		for schedule in scheduled_slots:
			out.append(schedule._serialized(recursive=True))
		return out

	def get_schedule_for_day(self,day_of_week):
		scheduled_slots = self.schedule_set.filter(day_of_week=day_of_week)
		out = []
		for schedule in scheduled_slots:
			out.append(schedule._serialized(recursive=True))
		return out


class Schedule(BaseModel):
	of_doctor = m.ForeignKey(Doctor, on_delete=m.CASCADE)
	slot_duration_min = m.FloatField(default=15.)
	day_of_week = m.CharField(max_length=15)


class WorkDay(BaseModel):
	of_schedule = m.ForeignKey(Schedule, on_delete=m.CASCADE)
	start_time = m.DateTimeField()
	end_time = m.DateTimeField()


