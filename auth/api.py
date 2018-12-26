from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.serializers import EmailVerifySerializer
from auth.serializers import PasswordChangeSerializer
from auth.serializers import ResendEmailConfirmationSertializer
from auth.serializers import ResetPasswordSerializer
from auth.serializers import SignInSerializer
from auth.serializers import SignUpSerializer
from users.models import User

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)


class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (IsAdminUser,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(SignUpAPIView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data_to_response = {
            'detail': _('Confirmation email successfully sent.')
        }
        data_to_response.update(serializer.data)
        return Response(
            data_to_response, status=status.HTTP_201_CREATED, headers=headers
        )


class EmailVerifyAPIView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return EmailVerifySerializer(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            '200': 'Email was verified',
            '400': 'Bad request.'
        },
        request_body=EmailVerifySerializer,
        operation_id='email_verify',
        operation_description='Email Verify.',
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        if token:
            data_to_response = EmailVerifySerializer({
                'email': token.user.email,
                'auth_token': token.key,
            }).data
            data_to_response['detail'] = _('Email was verified.')
            return Response(data_to_response, status=status.HTTP_200_OK, )
        return Response({
            'detail': _('Email was not verified.')
        },
            status=status.HTTP_400_BAD_REQUEST
        )


class SignInAPIView(APIView):
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(SignInAPIView, self).dispatch(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            '200': 'Successfully authenticated.',
            '400': 'Bad request.'
        },
        request_body=SignInSerializer,
        operation_id='sign_in',
        operation_description='Sign in.',
    )
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data.get('email'))
            data_to_response = {
                'auth_token': user.auth_token.key,
                'detail': _('Successfully authenticated.')
            }
            return Response(data_to_response, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response(e)


class ResendEmailConfirmationAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={
            '200': 'Email confirmation code successful sent.',
            '400': 'Bad request.'
        },
        request_body=ResendEmailConfirmationSertializer,
        operation_id='resend_email_confirmation',
        operation_description='Resend email confirmation.',
    )
    def post(self, request, *args, **kwargs):
        serializer = ResendEmailConfirmationSertializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={
            '200': 'Password reset email sent.',
            '400': 'Bad request.'
        },
        request_body=ResetPasswordSerializer,
        operation_id='password_reset_email_confirmation',
        operation_description='Password reset email.',
    )
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeAPIView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeAPIView, self).dispatch(*args, **kwargs)

    def get_serializer_context(self):
        return {'request': self.request}

    @swagger_auto_schema(
        responses={
            '200': 'Password change.',
            '400': 'Bad request.'
        },
        request_body=ResetPasswordSerializer,
        operation_id='password_change',
        operation_description='Password change.',
    )
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(
            context={
                'request': request,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})


class SignOutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        request.user.auth_token.delete()
        return Response({
            "detail": _("Successfully signed out.")},
            status=status.HTTP_200_OK
        )
