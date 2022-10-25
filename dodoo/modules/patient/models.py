from django.db import models as m
from ..base.models import BaseModel
from ..doctor import models as doctor


class Patient(BaseModel):
	of_doctor = m.ForeignKey(doctor.Doctor, on_delete=m.SET_NULL, null=True)

	@classmethod
	def get_medical_history(cls, patient_id):
		try:
			patient = Patient.objects.get(pk=patient_id)
			out = []
			for record in patient.medical_records_set.all():
				out.append(record._serialize(recursive=True))
			return out
		except ObjectDoesNotExist as odne:
			return []

	@classmethod
	def get_medical_record(cls, patient_id, record_id):
		try:
			patient = Patient.objects.get(pk=patient_id)
			record = patient.medical_records_set.get(pk=record_id)
			return record._serialize(recursive=True)
		except ObjectDoesNotExist as odne:
			return {}


class Medicine(BaseModel):
	chemical_name = m.CharField(max_length=127)
	dosage = m.FloatField(default=0.)
	unit = m.CharField(max_length=7, choices=[
		('ml', 'ml'),
		('mg', 'mg'),
	])


class MedicalRecord(BaseModel):
	of_patient = m.ForeignKey(Patient, on_delete=m.CASCADE)
	diagnosis = m.CharField(max_length=1023)
	instructions = m.CharField(max_length=2047)


class Medication(BaseModel):
	of_record = m.ForeignKey(MedicalRecord, on_delete=m.CASCADE)
	medicine = m.ForeignKey(Medicine, on_delete=m.SET_NULL, null=True)
	start_date = m.DateTimeField()
	end_date = m.DateTimeField()
	interval = m.FloatField(default=8.)


class ReportType(BaseModel):
	pass


class Report(BaseModel):
	of_record = m.ForeignKey(MedicalRecord, on_delete=m.CASCADE)
	type = m.ForeignKey(ReportType, on_delete=m.SET_NULL, null=True)
	report_file = m.FileField(upload_to='patient/medical_record/reports/')