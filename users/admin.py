# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User
from users.models import EmailConfirmation
from users.forms import UserChangeForm
from users.forms import UserCreationForm

admin.site.unregister(Group)


@admin.register(User)
class AdminUser(BaseUserAdmin):
    list_display = ('email', 'type', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('-id',)

    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (_('Personal info'), {'fields': ('email', 'type', 'password')}),
        (
            _('Permissions'), {'fields': (
                'is_active', 'is_staff', 'is_superuser',
            )},
        ),
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('name', 'password1', 'password2',),
            },
        ),
    )


@admin.register(EmailConfirmation)
class AdminEmailConfirmation(admin.ModelAdmin):
    list_display = ('email', 'used', 'confirmed')
    search_fields = ('email',)

    def has_add_permission(self, request):
        return False

