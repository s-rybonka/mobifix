import factory
from faker import Faker
from factory import fuzzy
from factory.django import DjangoModelFactory
from django.utils.crypto import get_random_string

from services.models import Order
from services.models import Service
from users.factories import UserFactory

faker = Faker()


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    name = faker.name()
    description = fuzzy.FuzzyText()


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    service = factory.SubFactory(ServiceFactory)
    user = factory.SubFactory(UserFactory)
    title = faker.name()
    number = get_random_string(5).upper()
