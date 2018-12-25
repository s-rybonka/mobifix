from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authtoken.models import Token

from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        from users.models import EmailConfirmation

        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(email, password, **extra_fields)
        Token.objects.create(user=user)
        EmailConfirmation.objects.create(
            user=user,
            email=user.email,
            key=get_random_string(5).upper(),
            used=True
        )
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)
