from django.db import models as m
from ..base.models import BaseModel
from ..doctor import models as doctor
from ..patient import models as patient


class Appointment(BaseModel):
	of_doctor = m.ForeignKey(doctor.Doctor, on_delete=m.CASCADE)
	of_patient = m.ForeignKey(patient.Patient, on_delete=m.CASCADE)
	scheduled_time = m.DateTimeField()
	type = m.CharField(max_length=63, choices=[
		('visit', 'Regular Checkup'),
		('followup', 'Requested Follow Up'),
		('report', 'Report Review'),
		('checkup', 'Routined Checkup'),
		('operation', 'Operation')
	])
	is_confirmed = m.BooleanField(default=False)
