from rest_framework import serializers
from ..models import Semester

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'is_active']
        extra_kwargs = {
            'name': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'is_active': {'required': True},
        }
