from django.db import models
from mixins.models import CreatedMixin


class Subscriber(CreatedMixin):
    email = models.EmailField(unique=True)
    gdpr_consent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Subskrybent'
        verbose_name_plural = 'Subskrybenci'


class SubscriberSMS(CreatedMixin):
    phone = models.CharField(max_length=20, unique=True)
    gdpr_consent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Subskrybent SMS'
        verbose_name_plural = 'Subskrybenci SMS'
