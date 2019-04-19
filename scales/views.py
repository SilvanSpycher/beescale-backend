from django.shortcuts import render

from rest_framework import viewsets

from .models import Measurement
from .serializers import MeasurementSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        return Measurement.objects.all()
