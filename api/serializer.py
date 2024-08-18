from rest_framework import serializers
from .models import Department,PatientRecords
from django.contrib.auth.models import User,Group



class RegisterUserSerializer(serializers.ModelSerializer):
    group = serializers.ChoiceField(choices=[('Patients', 'Patients'), ('Doctors', 'Doctors')],write_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(),required=True,write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email','group', 'department']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        group_name = validated_data.pop('group')
        department = validated_data.pop('department')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        
        # Add user to the specified group
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)

        # Associate the user with the specified department
        if group_name == 'Doctors':
            department.doctors.add(user)
        elif group_name == 'Patients':
            department.patients.add(user)

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# class RegisterSerializer(serializers.ModelSerializer):
#     group = serializers.ChoiceField(choices=[('Patients','Patients'),('Doctors','Doctors')])
#     department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

#     class Meta:
#         model = User
#         fields = ['username','password','email','group','department']

#     def create(self,validated_data):
#         group_name=validated_data.pop('group')
#         department = validated_data.pop('department')

#         user = User.objects.create_user(**validated_data)
#         group = Group.objects.get(name=group_name)
#         group.user_set.add(user)

#         if department == 'Doctors':
#             Department.doctors.add(user)
#         elif department == 'Patients':
#             Department.patients.add(user)

#         return user


# class DepartmentSerializer(serializers.ModelSerializer):
#     class meta:
#         model = Department
#         field = '__all__'

# class PatientRecordsSerializer(serializers.ModelSerializer):
#     class meta:
#         model = PatientRecords
#         field = '__all__'
    
class DoctorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='doctor-detail',lookup_field='pk')
    class Meta:
        model = User
        fields = ['id', 'username','url']
        # fields = "__all__"

class PatientsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='patient-detail',lookup_field='pk')
    class Meta:
        model = User
        fields = ['id', 'username','url']
        # fields = "__all__"



class DoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']
        
class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']

class PatientRecordsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='patient-record',lookup_field='pk')
    class Meta:
        model = PatientRecords
        fields = ['record_id','url','diagnostics','observations','treatments','misc','patient','department_id']

class DepartmentSerializer(serializers.ModelSerializer):
    doctor_url = serializers.HyperlinkedIdentityField(view_name='department-doctors',lookup_field='pk')
    patient_url = serializers.HyperlinkedIdentityField(view_name='department-patients',lookup_field='pk')
    class Meta:
        model = Department
        fields = "__all__"

class DepartmentDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
