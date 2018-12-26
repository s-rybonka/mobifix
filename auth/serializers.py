from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from users.models import EmailConfirmation
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from users.models import Profile


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    account_type = serializers.ChoiceField(choices=User.TYPES)
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, email):
        email = User.objects.normalize_email(email=email)
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                _("A user is already registered with this e-mail address.")
            )
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        account_type = self.validated_data.get('account_type')
        password = self.validated_data.get('password1')
        user_data = {
            'email': email,
            'type': account_type,
            'password': password,
        }
        user = User.objects.create_user(**user_data)
        confirmation_code = user.email_confirmations.last().key
        send_mail(
            subject=settings.EMAIL_SUBJECT_PREFIX + 'Email confirmation.',
            message='Hi there, your email confirmation code: {}'.format(
                confirmation_code
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(min_length=5, write_only=True)
    auth_token = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        confirmation_code = self.validated_data.get('confirmation_code')
        try:
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)
            email_confirmation = user.email_confirmations.get(key=confirmation_code, email=email)
            if email_confirmation and not email_confirmation.confirmed:
                email_confirmation.confirm_email()
                return token
        except (User.DoesNotExist, EmailConfirmation.DoesNotExist):
            raise ValidationError(
                _('Invalid credentials provided.')
            )


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if user:
            email_confirmation = user.email_confirmations.last()
            if email_confirmation and email_confirmation.confirmed:
                Token.objects.get_or_create(user=user)
                Profile.objects.get_or_create(user=user)
            else:
                raise PermissionDenied(
                    _('E-mail is not verified.'),
                )
        else:
            raise ValidationError(_('Unable to log in with provided credentials.'))
        return attrs


class ResendEmailConfirmationSertializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
            email_confirmation = user.email_confirmations.last()
            is_email_confirmed = email_confirmation.used and email_confirmation.confirmed
            if is_email_confirmed:
                raise ValidationError('E-mail:{email} already confirmed.'.format(email=email))
        except User.DoesNotExist as e:
            raise ValidationError(e)
        return attrs

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)

        email_confirmation = EmailConfirmation.objects.create(
            user=user,
            email=user.email,
            key=get_random_string(5).upper(),
            used=True
        )
        send_mail(
            subject=settings.EMAIL_SUBJECT_PREFIX + 'Resend Email confirmation.',
            message='Hi there, your new email confirmation code: {}'.format(
                email_confirmation.key
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            return email
        else:
            raise ValidationError(
                _('User with email ({}) does not exist.'.format(email))
            )

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        temp_password = get_random_string(8)
        user = User.objects.get(email=email)
        user.set_password(temp_password)
        user.save()
        send_mail(
            subject=settings.EMAIL_SUBJECT_PREFIX + 'Reset password.',
            message='Hi there, your new temp password: {}.'
                    'Please change it at your profile.'.format(temp_password),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password1 = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if user and not user.check_password(old_password):
            raise ValidationError(_('Invalid password.'))
        return old_password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data.get('password1')
        user.set_password(new_password)
        user.save()

