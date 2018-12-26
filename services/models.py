from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Service(TimeStampedModel):
    name = models.CharField(
        max_length=200,
        verbose_name=_('name'),
    )
    description = models.TextField(
        verbose_name=_('description'),
    )
    price = models.DecimalField(
        max_digits=9,
        verbose_name=_('price'),
        decimal_places=2,
        default=0,
    )
    currency = models.CharField(
        max_length=10,
        verbose_name=_('currency'),
        choices=settings.CURRENCIES,
        default=settings.CURRENCIES.UAH,
    )
    is_available = models.BooleanField(
        verbose_name=_('is available'),
        default=True,
    )

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return self.name


class Order(TimeStampedModel):

    STATUSES = Choices(
        ('unconfirmed', 'UNCONFIRMED', _('Unconfirmed')),
        ('pending', 'PENDING', _('Pending')),
        ('rejected', 'REJECTED', _('Rejected')),
        ('completed', 'COMPLETED', _('Completed')),
        ('returned', 'RETURNED', _('Returned')),
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_('title'),
    )
    number = models.CharField(
        max_length=5,
        verbose_name=_('number'),
        unique=True,
    )
    status = models.CharField(
        max_length=50,
        verbose_name=_('status'),
        choices=STATUSES,
        default=STATUSES.UNCONFIRMED,
    )
    service = models.ForeignKey(
        Service,
        verbose_name=_('service'),
        null=True,
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('user'),
        null=True,
        on_delete=models.SET_NULL,
    )
    notes = models.TextField(
        verbose_name=_('notes'),
        null=True,
        blank=True,
    )
    customer_first_name = models.CharField(
        max_length=100,
        verbose_name=_('customer first name'),
    )
    customer_last_name = models.CharField(
        max_length=100,
        verbose_name=_('customer last name'),
    )
    customer_phone = PhoneNumberField()
    phone_verification_code = models.CharField(
        max_length=5,
        verbose_name=_('phone verification code'),
    )
    is_phone_verified = models.BooleanField(
        verbose_name=_('is phone verified'),
        default=False,
    )

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return 'Order:{}'.format(self.number)
