import factory.fuzzy
from factory.django import DjangoModelFactory

from subscribers.models import Subscriber, SubscriberSMS
from mignow.utils import possible_numbers


class SubscriberFactory(DjangoModelFactory):
    email = factory.fuzzy.FuzzyText()
    gdpr_consent = False

    class Meta:
        model = Subscriber

    @factory.lazy_attribute_sequence
    def email(self, n):
        return f'test{n}@nowhere.nodomain'.lower()


class SubscriberSMSFactory(DjangoModelFactory):
    phone = factory.fuzzy.FuzzyText(length=9, chars=possible_numbers())
    gdpr_consent = False

    class Meta:
        model = SubscriberSMS
