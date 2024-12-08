from rest_framework import serializers
from ..models import Result
from . import StudentSerializer, CourseSerializer

class ResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Nested StudentSerializer
    course = CourseSerializer()  # Nested CourseSerializer

    class Meta:
        model = Result
        fields = ['student', 'course', 'score', 'grade', 'uploaded_at']
