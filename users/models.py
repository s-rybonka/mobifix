from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    TYPES = Choices(
        ('manager', 'MANAGER', _('Manager')),
        ('repairer', 'REPAIRER', _('Repairer')),
    )
    email = models.EmailField(verbose_name=_('email'), unique=True)
    type = models.CharField(verbose_name=_('type'), max_length=20, choices=TYPES)
    date_joined = models.DateTimeField(verbose_name=_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.',
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        raise NotImplementedError()

    def get_short_name(self):
        return ''

    @property
    def is_parent(self):
        return self.type == self.TYPES.PARENT


class EmailConfirmation(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        related_name='email_confirmations',
        on_delete=models.CASCADE,
    )
    email = models.EmailField(verbose_name=_('email'))
    key = models.CharField(verbose_name=_('key'), max_length=5)
    used = models.BooleanField(verbose_name=_('used'), default=False)
    confirmed = models.BooleanField(verbose_name=_('confirmed'), default=False)
    sent = models.DateTimeField(verbose_name=_('sent'), auto_now_add=True)

    class Meta:
        verbose_name = _('email confirmation')
        verbose_name_plural = _('email confirmations')

    def __str__(self):
        return self.email

    def confirm_email(self):
        self.confirmed = True
        self.save(update_fields=['confirmed',])