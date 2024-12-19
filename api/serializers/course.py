from rest_framework import serializers
from ..models import Course
from .semester import SemesterSerializer

class CourseSerializer(serializers.ModelSerializer):
    # Nested serializers for read operations
    semester = SemesterSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'semester', 'credit_units', 'description', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
            'code': {'required': True},
            'semester': {'required': True},
            'credit_units': {'required': True},
            'is_active': {'required': True},
        }
