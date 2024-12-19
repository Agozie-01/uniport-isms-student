from rest_framework import serializers
from ..models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'is_active': {'required': True},
        }
