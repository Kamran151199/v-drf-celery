from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class DataModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    user = models.ForeignKey(to=User, related_name='data', verbose_name=_('User'),
                             on_delete=models.CASCADE, null=False, blank=False)
    x_data_type = models.CharField(max_length=200, verbose_name=_('X Data Type'))
    y_data_type = models.CharField(max_length=200, verbose_name=_('Y Data Type'))


class PCorrelationModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    value = models.FloatField(verbose_name=_('Value'), null=False, blank=False)
    p_value = models.FloatField(verbose_name=_('P-Value'), null=False, blank=False)
    computed_at = models.DateTimeField(verbose_name=_('Calculated at'),
                                       auto_now_add=True, blank=False, null=False)
    data = models.ForeignKey(verbose_name=_('Related data'), to=DataModel,
                             related_name='correlations', on_delete=models.CASCADE, blank=False, null=False)
