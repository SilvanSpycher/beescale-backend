from django.urls import include, path

from rest_framework import routers

from .views import MeasurementViewSet

router = routers.SimpleRouter()
router.register(r'measurements', MeasurementViewSet, base_name='measurements')

urlpatterns = [
    path('', include(router.urls)),
    ]
