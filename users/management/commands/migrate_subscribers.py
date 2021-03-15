from django.core.management.base import BaseCommand
from subscribers.models import Subscriber, SubscriberSMS
from users.models import Client, User
from users.utils import write_to_csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.migrate_all_subscribers()

    def migrate_all_subscribers(self):
        self.migrate(Subscriber, 'email', 'phone')
        self.migrate(SubscriberSMS, 'phone', 'email')

    def migrate(self, model, first_field, second_field):
        column_names = ('id', first_field)
        csv_name = 'subscribers_conflicts.csv' if first_field == 'email' else 'subscribers_sms_conflicts.csv'

        for subscriber in model.objects.all().values(
                first_field, 'gdpr_consent').iterator():
            sub_first_field = {first_field: subscriber[first_field]}
            if not User.objects.filter(**sub_first_field).exists():
                client = Client.objects.filter(**sub_first_field).values(
                    'pk', 'phone', 'email').first()
                if client:
                    client_first_field = {first_field: client[first_field]}
                    client_second_field = {second_field: client[second_field]}
                    user_exist = User.objects.filter(
                        **client_second_field).exclude(
                            **client_first_field).exists()
                    if user_exist:
                        write_to_csv(csv_name, column_names,
                                     (client['pk'], client[first_field]))
                    if not user_exist:
                        if Client.objects.filter(
                                phone=client['phone']).count() == 1:
                            User.objects.create(
                                **client_first_field,
                                **client_second_field,
                                gdpr_consent=subscriber['gdpr_consent'])
                        else:
                            write_to_csv(csv_name, column_names,
                                         (client['pk'], client[first_field]))
                else:
                    User.objects.create(
                        **sub_first_field,
                        **{second_field: ''},
                        gdpr_consent=subscriber['gdpr_consent'])
