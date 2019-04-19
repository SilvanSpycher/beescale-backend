from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Setting(models.Model):
    sending_rate = models.IntegerField(_('sending_rate'))

    def __str__(self):
        if self.scale:
            return str(self.scale)
        else:
            return "NO SCALE"


class Scale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_('scale name'), max_length=40, default='Scale')
    settings = models.OneToOneField(Setting, on_delete=models.SET_NULL, null=True, blank=True, related_name='scale')

    def __str__(self):
        return str(self.user) + " " + self.name


class Measurement(models.Model):
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    time = models.DateTimeField(_('measurement time'))
    weight = models.FloatField(_('measurement weight'))

    def __str__(self):
        return str(self.scale) + " " + str(self.time)
