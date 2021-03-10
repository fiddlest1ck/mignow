from django.db import models

from mixins.models import CreatedMixin


class User(CreatedMixin):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gdpr_consent = models.BooleanField()

    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'


class Client(CreatedMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienci'
