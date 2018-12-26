import io

from rest_framework.parsers import JSONParser
from rest_framework.test import APITestCase as DRF_APITestCase
from users.models import User


class APITestCase(DRF_APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='12345678',
        )

    def set_auth_headers(self, token_key=None, **extra_headers):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + token_key,
            **extra_headers,
        )

    def unset_auth_headers(self):
        self.client.credentials()

    @classmethod
    def parse_response(cls, response_data):
        stream = io.BytesIO(response_data)
        data = JSONParser().parse(stream)
        return data
