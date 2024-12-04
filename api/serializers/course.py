from rest_framework import serializers
from ..models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'department', 'session', 'credit_units', 'description', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
            'code': {'required': True},
            'department': {'required': True},
            'session': {'required': True},  # Ensure session is required if it's critical
            'credit_units': {'required': True},
            'is_active': {'required': True},
        }
