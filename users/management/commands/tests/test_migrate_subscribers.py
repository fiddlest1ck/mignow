import pytest
from unittest.mock import patch

from django.core.management import call_command

from users.models import User
from users.tests.factories import UserFactory, ClientFactory
from subscribers.tests.factories import SubscriberFactory, SubscriberSMSFactory


class TestSubscriberMigrate:

    @pytest.mark.django_db
    def test_user_with_same_phone_doesnt_exists(self):
        subscriber = SubscriberFactory.create()
        client = ClientFactory.create(email=subscriber.email)
        call_command('migrate_subscribers')
        assert User.objects.filter(
            email=client.email,
            phone=client.phone).exists() is True

    @pytest.mark.django_db
    @patch('users.management.commands.migrate_subscribers.write_to_csv')
    def test_user_with_same_phone_exists(self, mock_write):
        subscriber = SubscriberFactory.create()
        client = ClientFactory.create(email=subscriber.email)
        UserFactory(email='test@zly1.pl', phone=client.phone)
        call_command('migrate_subscribers')
        mock_write.assert_called()

    @pytest.mark.django_db
    def test_client_with_same_email_doesnt_exists(self):
        SubscriberFactory.create()
        ClientFactory.create(email='test@zly2.pl')
        call_command('migrate_subscribers')
        assert User.objects.filter(phone='').exists() is True

    @pytest.mark.django_db
    @patch('users.management.commands.migrate_subscribers.write_to_csv')
    def test_len_of_clients_with_phone_is_gt_one(self, mock_write):
        subscriber = SubscriberFactory.create()
        # non unique
        client = ClientFactory.create(email=subscriber.email)
        ClientFactory.create(phone=client.phone)
        call_command('migrate_subscribers')
        assert User.objects.filter(
            email=client.email,
            phone=client.phone).exists() is False

    @pytest.mark.django_db
    def test_user_with_same_email_exists(self):
        subscriber = SubscriberFactory.create()
        UserFactory(email=subscriber.email)
        len_of_users = User.objects.filter().count()
        call_command('migrate_subscribers')
        assert User.objects.filter().count() == len_of_users


class TestSubscriberSMSMigrate:

    @pytest.mark.django_db
    def test_user_with_same_email_doesnt_exists(self):
        subscriber = SubscriberSMSFactory.create()
        client = ClientFactory.create(phone=subscriber.phone)
        call_command('migrate_subscribers')
        assert User.objects.filter(
            email=client.email,
            phone=client.phone).exists() is True

    @pytest.mark.django_db
    @patch('users.management.commands.migrate_subscribers.write_to_csv')
    def test_user_with_same_email_exists(self, mock_write):
        subscriber = SubscriberSMSFactory.create()
        client = ClientFactory.create(phone=subscriber.phone)
        UserFactory(phone='123123142', email=client.email)
        call_command('migrate_subscribers')
        mock_write.assert_called()

    @pytest.mark.django_db
    def test_client_with_same_number_doesnt_exists(self):
        SubscriberSMSFactory.create()
        ClientFactory.create(phone='123123142')
        call_command('migrate_subscribers')
        assert User.objects.filter(email='').exists() is True

    @pytest.mark.django_db
    @patch('users.management.commands.migrate_subscribers.write_to_csv')
    def test_len_of_clients_with_phone_is_gt_one(self, mock_write):
        subscriber = SubscriberSMSFactory.create()
        # non unique
        client = ClientFactory.create(phone=subscriber.phone)
        ClientFactory.create(phone=client.phone)
        call_command('migrate_subscribers')
        assert User.objects.filter(
            email=client.email,
            phone=client.phone).exists() is False

    @pytest.mark.django_db
    def test_user_with_same_phone_exists(self):
        subscriber = SubscriberSMSFactory.create()
        UserFactory(phone=subscriber.phone)
        len_of_users = User.objects.filter().count()
        call_command('migrate_subscribers')
        assert User.objects.filter().count() == len_of_users
