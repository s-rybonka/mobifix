import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from django.utils.crypto import get_random_string

from services.models import Order
from services.models import Service
from users.factories import UserFactory


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    name = factory.LazyAttribute(lambda o: 'name_%s' % o.name)
    description = fuzzy.FuzzyText()


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    service = factory.SubFactory(ServiceFactory)
    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda o: 'title_%s' % o.name)
    number = get_random_string(5).upper()
    customer_first_name = factory.LazyAttribute(lambda o: 'c_f_name_%s' % o.name)
    customer_last_name = factory.LazyAttribute(lambda o: 'c_l_name_%s' % o.name)
