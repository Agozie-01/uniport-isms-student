from rest_framework import serializers
from ..models import Student
from .department import DepartmentSerializer

class StudentSerializer(serializers.ModelSerializer):
       # Nested serializers for read operations
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'level', 'matric_number', 'department', 'email', 'status', 'date_of_birth', 'created_at']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'matric_number': {'required': True},
            'department': {'required': True},  # Change to False if optional
            'email': {'required': True},
            'level': {'required': True},
            'status': {'required': False},
            'date_of_birth': {'required': True},  # Change to False if optional
        }