from django.contrib.auth.models import User

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return User.objects.none()
        elif self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)
