from django.core.management.base import BaseCommand
from subscribers.models import Subscriber, SubscriberSMS
from users.models import Client, User
from users.utils import gen_value, write_to_csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.migrate_all_subscribers()

    def migrate_all_subscribers(self):
        self.migrate(Subscriber, 'email', 'phone')
        self.migrate(SubscriberSMS, 'phone', 'email')

    def migrate(self, model, first_field, second_field):
        column_names = ('id', first_field)
        csv_name = 'subscribers_conflicts.csv' if first_field == 'email' else 'subscribers_sms_conflicts.csv'

        for subscriber in model.objects.all():
            if not User.objects.filter(**gen_value(subscriber, first_field)):
                client = Client.objects.filter(
                    **gen_value(subscriber, first_field))
                if client.exists():
                    client = client.first()
                    user = User.objects.filter(
                        **gen_value(client, second_field)).exclude(
                            **gen_value(client, first_field))
                    len_of_clients = Client.objects.filter(
                        phone=client.phone).count()
                    if user:
                        write_to_csv(
                            csv_name, column_names,
                            (client.pk, gen_value(
                             client, first_field)[first_field]))
                    if not user:
                        if len_of_clients == 1:
                            User.objects.create(
                                **gen_value(client, first_field),
                                **gen_value(client, second_field),
                                gdpr_consent=subscriber.gdpr_consent)
                        else:
                            write_to_csv(csv_name, column_names,
                                         (client.pk, gen_value(
                                          client, first_field)[first_field]))
                else:
                    User.objects.create(**gen_value(subscriber, first_field),
                                        **{second_field: ''},
                                        gdpr_consent=subscriber.gdpr_consent)
