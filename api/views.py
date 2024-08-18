from rest_framework import generics, permissions
from .models import User,PatientRecords,Department
from .serializer import( DoctorSerializer,RegisterUserSerializer,
    DoctorSerializer,DoctorDetailSerializer,
    LoginSerializer,PatientsSerializer,PatientDetailSerializer,
    PatientRecordsSerializer,DepartmentSerializer,DepartmentDoctorSerializer
)
from oauth2_provider.models import AccessToken,Application
from oauth2_provider.views import TokenView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from .permissions import IsDoctor,IsSelf,IsDoctorOrIsSelf,IsDoctorInSameDepartment


from django.contrib.auth import authenticate,login,logout
import datetime
import jwt
from rest_framework.permissions import IsAuthenticated

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is None:
            raise AuthenticationFailed('User not found')

        # Login the user
        login(request, user)

        # Generate JWT token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),  # Token expiration time
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Create response
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        logout(request)
        response.data = {
            'message':'successfully logged out'
        }
        return response


class RegisterCreateView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

class DoctorListView(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='Doctors')
    print(User.objects.filter(groups__name='Doctors'))
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    

class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='Doctors')
    serializer_class = DoctorDetailSerializer
    permission_classes = [IsAuthenticated, IsDoctor,IsSelf]
    lookup_field = 'pk'
    

class PatientsListView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = PatientsSerializer
    queryset = User.objects.filter(groups__name="Patients")
    

class PatientsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDoctorOrIsSelf,IsAuthenticated]
    serializer_class = PatientDetailSerializer
    queryset = User.objects.filter(groups__name="Patients")
    lookup_field = 'pk'

class PatientRecordsListView(generics.ListAPIView):
    permission_classes = [IsDoctorInSameDepartment]
    serializer_class = PatientRecordsSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return PatientRecords.objects.all()
        user = self.request.user
        return PatientRecords.objects.filter(department_id__doctors = user)

class PatientRecordsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsDoctorOrIsSelf]
    serializer_class=PatientRecordsSerializer
    lookup_field='pk'
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PatientRecords.objects.all()

        return PatientRecords.objects.filter(department_id__doctors = user) | PatientRecords.objects.filter(patient=user)

class DepartmentListView(generics.ListAPIView):
    serializer_class=DepartmentSerializer
    queryset = Department.objects.all()

class DepartmentDoctorsView(generics.ListAPIView):
    serializer_class = DepartmentDoctorSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError("Department not found")
        return department.doctors.all()

class DepartmentPatientsView(generics.ListAPIView):
    serializer_class = DepartmentDoctorSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        department = Department.objects.get(pk=department_id)
        return department.patients.all()
            
# class DepartmentPatientsView(generics.RetrieveUpdateAPIView):
#     serializer_class = DepartmentDoctorSerializer  # Ensure this is the correct serializer

#     def get_queryset(self):
#         department_id = self.kwargs.get('pk')
        
#         # Debugging: Print the department_id to ensure it's being passed correctly
#         print(f"Department ID: {department_id}")
        
#         try:
#             # Try to get the department by id
#             department = Department.objects.get(pk=department_id)
#             print(f"Department found: {department.name}")
#         except Department.DoesNotExist:
#             raise NotFound(f"Department with id {department_id} does not exist.")

#         # Return the patients related to this department
#         patients = department.patients.all()
#         print(patients)
#         print(f"Patients found: {patients.count()}")  # Debugging: Number of patients found
#         return patients

# @method_decorator(csrf_exempt, name='dispatch')
# class LoginView(APIView):
#     def post(self,request):
#         username=request.data.get('username')
#         password=request.data.get('password')
#         user = authenticate(username=username,password=password)

#         if user is not None:
#             application = Application.objects.get(name="oauth-api")  # Replace with your app name
#             token_view = TokenView()
#             token_request = request._request
#             token_request.POST = token_request.POST.copy()
#             token_request.POST['grant_type'] = 'password'
#             token_request.POST['username'] = username
#             token_request.POST['password'] = password
#             token_request.POST['client_id'] = application.client_id
#             token_request.POST['client_secret'] = application.client_secret
            
#             response = token_view.post(token_request)
#             return response
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         try:
#             refresh_token = request.COOKIES.get('jwt')
#             if refresh_token:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()
#             response = Response({'message': 'success'}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             response = Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return response

# from django.http import HttpResponseRedirect
# from rest_framework import status

# class LogoutView(APIView):
#     def post(self, request):
#         try:
#             response = Response()
#             response.delete_cookie('jwt')
#             return Response({'success':'user logged out '},status=status.HTTP_200_OK)
#             # return HttpResponseRedirect('/login/')
#         except Exception as e:
#             return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class DoctorListCreateView(generics.RetrieveAPIView):
#     queryset =User.objects.all()
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'pk'

    # def get_queryset(self):
    #     # Filter users who are in the "Doctors" group
    #     return User.objects.filter(groups__name='Doctors')
    
    # def get(self, request, *args, **kwargs):
    #     return 

    # def post(self, request, *args, **kwargs):
    #     # Ensure that only users in the "Doctors" group can post
    #     # if not request.user.groups.filter(name='Doctors').exists():
    #     #     return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    #     return super().post(request, *args, **kwargs)