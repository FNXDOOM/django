# alerts/serializers.py
from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = [
            'id',
            'timestamp',
            'violation_type',
            'camera_id',
            'snapshot',
            'clip',
            'summary',   # <-- Add this line
        ]
