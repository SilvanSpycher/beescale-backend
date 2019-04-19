from rest_framework import serializers

from .models import Setting, Scale, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'scale', 'time', 'weight')
