from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import Client, User
from subscribers.models import Subscriber, SubscriberSMS


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.update_gdpr_consent()

    @transaction.atomic
    def update_gdpr_consent(self):

        for user in User.objects.all():
            subscriber = Subscriber.objects.filter(email=user.email).first()
            subscriber_sms = SubscriberSMS.objects.filter(phone=user.phone).first()
            if subscriber_sms or subscriber:
                if Client.objects.filter(email=user.email, phone=user.phone).exists():
                    newest = sorted([(subscriber, subscriber.create_date),
                                    (subscriber_sms, subscriber_sms.create_date),
                                    (user, user.create_date)], key=lambda x: x[1], reverse=True)[0]
                    user.gdpr_consent = newest[0].gdpr_consent
                    user.save()
                elif subscriber and user.create_date < subscriber.create_date:
                    user.gdpr_consent = subscriber.gdpr_consent
                    user.save()
                elif subscriber_sms and user.create_date < subscriber_sms.create_date:
                    user.gdpr_consent = subscriber_sms.gdpr_consent
                    user.save()
