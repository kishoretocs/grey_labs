from django.contrib import admin
from .models import Department,PatientRecords
# Register your models here.

admin.site.register(PatientRecords)
admin.site.register(Department)