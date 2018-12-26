import factory
from faker import Faker
from django.utils.crypto import get_random_string
from factory.django import DjangoModelFactory

from users.models import Profile
from users.models import User
from users.models import EmailConfirmation

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = faker.email()
    type = factory.Iterator([User.TYPES, ])


class EmailConfirmationFactory(DjangoModelFactory):
    class Meta:
        model = EmailConfirmation

    user = factory.SubFactory(UserFactory)
    email = faker.email()
    key = get_random_string(5).upper()


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    first_name = faker.name()
    last_name = faker.name()
    address = faker.name()
    facebook = faker.name()
    twitter = faker.name()
