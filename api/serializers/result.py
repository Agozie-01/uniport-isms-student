from rest_framework import serializers
from ..models import Result
from .student import StudentSerializer
from .course import CourseSerializer

class ResultSerializer(serializers.ModelSerializer):
    # Nested serializers for read operations
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Result
        fields = [
            'id',
            'student',
            'course',
            'score',
            'grade',
            'gp',
            'qp',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'grade', 'gp', 'qp']

    def create(self, validated_data):
        """
        Override create to handle nested input if needed.
        """
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Override update to handle nested input if needed.
        """
        return super().update(instance, validated_data)
