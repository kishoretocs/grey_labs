from django.db import models
from django.contrib.auth.admin import User

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    diagnostics = models.TextField()
    location = models.CharField(max_length=255)
    specialization = models.CharField(max_length=100)
    doctors = models.ManyToManyField(User,related_name='department_as_doctor',blank=True,null=True)
    patients = models.ManyToManyField(User,related_name='department_as_patient',blank=True,null=True)

    def __str__(self):
        return self.name
        
class PatientRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='patient_records')
    created_date = models.DateTimeField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department_id = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name='patient_records')
    misc = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'Records {self.record_id} for {self.patient.username}'

        