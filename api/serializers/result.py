from rest_framework import serializers
from ..models import Result

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['student', 'course', 'score', 'grade', 'uploaded_at']
