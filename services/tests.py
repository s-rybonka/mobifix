from unittest.mock import patch

from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token

from services.factories import OrderFactory
from services.factories import ServiceFactory
from services.models import Order
from users.factories import UserFactory
from utils.tests import APITestCase


class ServiceAPITestCase(APITestCase):
    fixtures = ['services', ]

    @classmethod
    def setUpTestData(cls):
        cls.services_url = reverse('api:services:services')
        cls.orders_url = reverse('api:services:orders-list')
        cls.employee = UserFactory()
        Token.objects.get_or_create(user=cls.employee)

    def test_can_users_get_service_list(self):
        response = self.client.get(self.services_url)
        self.assertEqual(response.status_code, 200)
        data = self.parse_response(response.content)
        self.assertEqual(data['count'], 7)  # data from services.json fixture.

    def test_can_employee_get_order_list(self):
        self.set_auth_headers(token_key=self.employee.auth_token.key)
        for i in range(10):
            OrderFactory(number=get_random_string(5).upper())

        response = self.client.get(self.orders_url)
        data = self.parse_response(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 10)

    @patch('users.models.User.send_sms', return_value=0)
    def test_can_employee_create_new_order(self, send_sms):
        self.set_auth_headers(
            token_key=self.employee.auth_token.key,
        )
        post_data = {
            'title': 'Lorem',
            'service': ServiceFactory().id,
            'notes': 'Test details about order',
            'customer_first_name': 'Test first name',
            'customer_last_name': 'Test last name',
            'customer_phone': '+380978145561',
        }

        response = self.client.post(self.orders_url, data=post_data)

        data = self.parse_response(response.content)

        order = Order.objects.last()

        self.assertEqual(data['title'], order.title)
        self.assertEqual(data['number'], order.number)
        self.assertEqual(data['status'], order.status)
        self.assertEqual(data['service'], order.service.id)
        self.assertEqual(data['notes'], order.notes)
        self.assertEqual(data['customer_first_name'], order.customer_first_name)
        self.assertEqual(data['customer_last_name'], order.customer_last_name)
        self.assertEqual(data['customer_phone'], order.customer_phone)
        self.assertFalse(data['is_phone_verified'])

    def test_can_employee_update_order(self):
        self.set_auth_headers(
            token_key=self.employee.auth_token.key,
        )
        order = OrderFactory()
        partial_post_data = {
            'title': 'New Order Title',
            'number': 'DFGHR',
            'service': ServiceFactory().id,
            'status': Order.STATUSES.PENDING,
        }
        order_detail_url = reverse(
            'api:services:orders-detail', kwargs={
                'pk': order.pk
            }
        )

        response = self.client.patch(order_detail_url, partial_post_data)

        self.assertEqual(response.status_code, 200)

        data = self.parse_response(response.content)
        order.refresh_from_db()

        self.assertEqual(order.title, data['title'])
        self.assertEqual(order.service.id, data['service'])
        self.assertEqual(order.status, data['status'])

    @patch('users.models.User.send_sms', return_value='XXXXX')
    def test_can_employee_confirm_order(self, send_sms):
        self.set_auth_headers(
            token_key=self.employee.auth_token.key,
        )
        order_data = {
            'title': 'New Order Title',
            'number': 'DFGHR',
            'service': ServiceFactory(),
            'customer_first_name': 'Test first name',
            'customer_last_name': 'Test last name',
            'customer_phone': '+380978145561',
            'phone_verification_code': 'XXXXX',
        }
        order = OrderFactory(**order_data)
        order_confirm_url = reverse(
            'api:services:orders-confirm-order',
            kwargs={
                'pk': order.pk
            }
        )

        response = self.client.patch(
            order_confirm_url,
            data={
                'verification_code': 'XXXXX',
                'status': Order.STATUSES.PENDING,
            }
        )

        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        data = self.parse_response(response.content)

        self.assertTrue(order.is_phone_verified)
        self.assertEqual(order.status, Order.STATUSES.PENDING)
        self.assertTrue(data['is_phone_verified'])

    def test_can_anonymous_get_public_order_data(self):
        order = OrderFactory(number='WWWXX', status=Order.STATUSES.COMPLETED)

        public_order_detail_url = reverse('api:services:order_public_detail')
        query_params = {
            'order_number': 'WWWXX'
        }

        response = self.client.get(public_order_detail_url, data=query_params)

        self.assertEqual(response.status_code, 200)
        data = self.parse_response(response.content)

        self.assertEqual(order.title, data['title'])
        self.assertEqual(order.number, data['number'])
        self.assertEqual(order.status, data['status'])
