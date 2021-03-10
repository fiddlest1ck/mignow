from django.db import models


class CreatedMixin(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
