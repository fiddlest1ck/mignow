import factory.fuzzy
from factory.django import DjangoModelFactory

from mignow.utils import possible_numbers

from users.models import User, Client


class UserFactory(DjangoModelFactory):
    email = factory.fuzzy.FuzzyText()
    phone = factory.fuzzy.FuzzyText(length=9, chars=possible_numbers())
    gdpr_consent = False

    class Meta:
        model = User

    @factory.lazy_attribute_sequence
    def email(self, n):
        return f'test_{n}@nowhere.nodomain'.lower()


class ClientFactory(DjangoModelFactory):
    phone = factory.fuzzy.FuzzyText(length=9, chars=possible_numbers())
    email = factory.fuzzy.FuzzyText()

    class Meta:
        model = Client

    @factory.lazy_attribute_sequence
    def email(self, n):
        return f'test_{n}@nowhere.nodomain'.lower()
