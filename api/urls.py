from django.urls import path
from .views import (
    RegisterCreateView,LoginView,LogoutView,DoctorListView,DoctorDetailView,
    PatientsListView,PatientsDetailView,PatientRecordsListView,PatientRecordsDetailView,
    DepartmentListView,DepartmentDoctorsView,DepartmentPatientsView
    )
urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('doctors/',DoctorListView.as_view(),name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),

    path('patients/',PatientsListView.as_view(),name='patient-list'),
    path('patients/<int:pk>/',PatientsDetailView.as_view(),name='patient-detail'),

    path('patient_records/',PatientRecordsListView.as_view(),name='patient-record-list'),
    path('patient_records/<int:pk>',PatientRecordsDetailView.as_view(),name='patient-record'),

    path('departments/',DepartmentListView.as_view(),name='department-list'),
    path('department/<int:pk>/doctors/', DepartmentDoctorsView.as_view(), name='department-doctors'),
    path('department/<int:pk>/patients/', DepartmentPatientsView.as_view(), name='department-patients'),

]