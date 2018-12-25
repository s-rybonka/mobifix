from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Service(TimeStampedModel):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    price = models.DecimalField(
        max_digits=9,
        verbose_name=_('price'),
        decimal_places=2,
    )
    currency = models.CharField(
        max_length=10,
        verbose_name=_('currency'),
        choices=settings.CURRENCIES,
        default=settings.CURRENCIES.UAH,
    )
    is_available = models.BooleanField(verbose_name=_('is available'), default=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return self.name
