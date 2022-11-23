from django.db import models as m
from ..patient import models as patient
from ..base.models import BaseModel


class Symptom(BaseModel):
	pass


class Diagnosis(BaseModel):
	symptoms = m.ManyToManyField(Symptom)


class Prescription(BaseModel):
	diagnoses = m.ForeignKey(Diagnosis, on_delete=m.CASCADE)
	tests = m.ManyToManyField(patient.Report)
	medications = m.ManyToManyField(patient.Medication)

