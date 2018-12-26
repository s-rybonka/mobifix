from django.core import mail
from django.core.urlresolvers import reverse

from users.factories import EmailConfirmationFactory
from users.factories import UserFactory
from users.models import User
from utils.tests import APITestCase


class AuthAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sign_up_url = reverse('api:auth:sign_up')
        cls.sign_in_url = reverse('api:auth:sign_in')
        cls.email_verify_url = reverse('api:auth:email_verify')

    def test_can_admin_register_employee(self):
        self.set_auth_headers(token_key=self.admin.auth_token.key)
        post_data = {
            'email': 'demo_employee@example.com',
            'account_type': User.TYPES.MANAGER,
            'password1': '12345678',
            'password2': '12345678',
        }
        response = self.client.post(
            self.sign_up_url,
            data=post_data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)

        user = User.objects.last()

        self.assertEqual(post_data.get('email'), user.email)
        self.assertEqual(post_data.get('account_type'), user.type)

        self.unset_auth_headers()

        response = self.client.post(
            self.sign_up_url,
            data=post_data
        )

        self.assertEqual(response.status_code, 401)

    def test_can_employee_sign_in(self):
        user = UserFactory(
            email='demo_acc@example.com',
        )
        email_confirmation = EmailConfirmationFactory(user=user)

        user.set_password('12345678')
        user.save()

        post_data = {
            'email': 'demo_acc@example.com',
            'password': '12345678',
        }

        response = self.client.post(
            self.sign_in_url,
            data=post_data,
        )
        user.refresh_from_db()
        data = self.parse_response(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data['detail'],
            'E-mail was not verified.'
        )

        email_confirmation.confirmed = True
        email_confirmation.save()
        email_confirmation.refresh_from_db()

        response = self.client.post(
            self.sign_in_url,
            data=post_data,
        )
        data = self.parse_response(response.content)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            user.auth_token.key,
            data['auth_token']
        )
        self.assertEqual(
            data['detail'],
            'Successfully authenticated.'
        )

    def test_can_employee_verify_email(self):
        user = UserFactory(
            email='demo_acc@example.com',
        )
        email_confirmation = EmailConfirmationFactory(user=user, email=user.email)

        post_data = {
            'email': user.email,
            'confirmation_code': email_confirmation.key,
        }

        response = self.client.post(self.email_verify_url, data=post_data)

        self.assertEqual(response.status_code, 200)

        data = self.parse_response(response.content)

        self.assertEqual(
            data['auth_token'],
            user.auth_token.key
        )
        self.assertEqual(
            data['email'],
            user.email
        )
