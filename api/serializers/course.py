from rest_framework import serializers
from ..models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'matric_number', 'department', 'email', 'date_of_birth', 'created_at']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'matric_number': {'required': True},
            'department': {'required': True},  # Change to False if optional
            'email': {'required': True},
            'date_of_birth': {'required': False},  # Change to False if optional
        }