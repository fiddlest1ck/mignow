import pytest
from django.core.management import call_command
from freezegun import freeze_time
from subscribers.tests.factories import SubscriberFactory, SubscriberSMSFactory
from users.models import User
from users.tests.factories import ClientFactory, UserFactory


class TestUpdateGdprConsent:
    @freeze_time(auto_tick_seconds=15)
    @pytest.mark.django_db
    def test_with_client_exists(self):
        user = UserFactory.create()
        ClientFactory.create(email=user.email, phone=user.phone)
        SubscriberFactory.create(email=user.email)
        SubscriberSMSFactory.create(phone=user.phone, gdpr_consent=True)

        call_command('update_gdpr_consent')

        assert User.objects.get(pk=user.pk).gdpr_consent is True

    @freeze_time(auto_tick_seconds=15)
    @pytest.mark.django_db
    def test_subscriber_is_newest(self):
        user = UserFactory.create()
        SubscriberFactory.create(email=user.email, gdpr_consent=True)

        call_command('update_gdpr_consent')

        assert User.objects.get(pk=user.pk).gdpr_consent is True

    @freeze_time(auto_tick_seconds=15)
    @pytest.mark.django_db
    def test_subscriber_sms_is_newest(self):
        user = UserFactory.create()
        SubscriberSMSFactory.create(phone=user.phone, gdpr_consent=True)

        call_command('update_gdpr_consent')
        assert User.objects.get(pk=user.pk).gdpr_consent is True

    @freeze_time(auto_tick_seconds=15)
    @pytest.mark.django_db
    def test_subscriber_sms_is_older(self):
        subscriber = SubscriberSMSFactory.create(phone='123123123',
                                                 gdpr_consent=True)
        user = UserFactory.create(phone=subscriber.phone)

        call_command('update_gdpr_consent')
        assert User.objects.get(pk=user.pk).gdpr_consent is False
