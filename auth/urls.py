from django.conf.urls import url

from auth import api as api_views

urlpatterns = (
    url(r'^sign-up/',
        api_views.SignUpAPIView.as_view(), name='sign_up'),
    url(r'^sign-in/',
        api_views.SignInAPIView.as_view(), name='sign_in'),
    url(r'^sign-out/',
        api_views.SignOutAPIView.as_view(), name='sign_out'),
    url(r'^email-verify/',
        api_views.EmailVerifyAPIView.as_view(), name='email_verify'),
    url(r'^resend-email-confirmation/',
        api_views.ResendEmailConfirmationAPIView.as_view(), name='resend_email_confirmation'),
    url(r'^password-reset/',
        api_views.PasswordResetAPIView.as_view(), name='password_reset'),
    url(r'^password-change/',
        api_views.PasswordChangeAPIView.as_view(), name='password_change'),
)
