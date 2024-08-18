from rest_framework.permissions import BasePermission
from django.contrib.auth.admin import User
from .models import Department,PatientRecords


class IsAdminUser(BasePermission):
    def has_permission(self,request,view):
        return bool(request.user and request.user.is_staff)

class IsDoctor(BasePermission):
    def has_permission(self,request,view):
        is_admin = IsAdminUser().has_permission(request,view)
        return is_admin or request.user.groups.filter(name='Doctors').exists()

class IsSelf(BasePermission):
    def has_object_permission(self,request,view,obj):
        if IsAdminUser().has_permission(request,view):
            return True
        return obj == request.user

class IsDoctorOrIsSelf(BasePermission):
    def has_permission(self,request,view):
        
        if IsAdminUser().has_permission(request,view):
            return True

        is_docotor = IsDoctor().has_permission(request,view)
        is_self = False
        if hasattr(view,'get_object'):
            obj = view.get_object()
            is_self = IsSelf().has_object_permission(request,view,obj)
        return is_docotor or is_self

class IsDoctorInSameDepartment(BasePermission):
    def has_permission(self,request,view):
        if IsAdminUser().has_permission(request,view):
            return True
        return is_admin or request.user.groups.filter(name='Doctors').exists()
    def has_object_permission(self,request,view,obj):
        return obj.department_id.doctors.filter(id= request.user.id).exists()