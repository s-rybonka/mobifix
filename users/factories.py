import factory
from factory.django import DjangoModelFactory

from users.models import Profile
from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.name)
    type = factory.Iterator([User.TYPES, ])


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile
    user = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda o: 'first_name_%s' % o.name)
    last_name = factory.LazyAttribute(lambda o: 'last_name_%s' % o.name)
    address = factory.LazyAttribute(lambda o: 'address%s' % o.name)
    facebook = factory.LazyAttribute(lambda o: 'facebook_%s' % o.name)
    twitter = factory.LazyAttribute(lambda o: 'twitter_%s' % o.name)
