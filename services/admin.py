from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from services.models import Order
from services.models import Service


@admin.register(Service)
class AdminService(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'is_available')


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('number', 'service', 'user',)
    readonly_fields = (
        'number', 'phone_verification_code', 'is_phone_verified', 'customer_phone',
    )

    fieldsets = (
        (_('Order details'), {'fields': ('number', 'status', 'service', 'user', 'notes')}),
        (
            _('Customer details'), {'fields': (
                'customer_first_name', 'customer_last_name', 'customer_phone',
                'phone_verification_code', 'is_phone_verified'
            )},
        ),
    )
