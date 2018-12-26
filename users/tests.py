from django.shortcuts import reverse
from rest_framework.authtoken.models import Token

from users.factories import ProfileFactory
from users.factories import UserFactory
from utils.tests import APITestCase


class UserAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employee = UserFactory()
        cls.profile = ProfileFactory(user=cls.employee)
        Token.objects.get_or_create(user=cls.employee)
        cls.profile_url = reverse('api:users:profile')

    def test_can_user_get_profile(self):
        self.set_auth_headers(token_key=self.employee.auth_token.key)

        response = self.client.get(self.profile_url)
        data = self.parse_response(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.profile.first_name, data['first_name'])
        self.assertEqual(self.profile.last_name, data['last_name'])
        self.assertEqual(self.profile.address, data['address'])
        self.assertEqual(self.profile.phone, data['phone'])
        self.assertEqual(self.profile.facebook, data['facebook'])
        self.assertEqual(self.profile.twitter, data['twitter'])

    def test_can_user_update_profile(self):
        self.set_auth_headers(token_key=self.employee.auth_token.key)
        partial_post_data = {
            'first_name': 'New First Name',
            'last_name': 'New Last Name',
            'address': 'New test address',
        }

        response = self.client.patch(self.profile_url, data=partial_post_data)

        self.assertEqual(response.status_code, 200)
        data = self.parse_response(response.content)

        self.employee.profile.refresh_from_db()
        self.assertEqual(
            self.employee.profile.first_name,
            data['first_name']
        )
        self.assertEqual(
            self.employee.profile.last_name,
            data['last_name']
        )
        self.assertEqual(
            self.employee.profile.address,
            data['address']
        )
