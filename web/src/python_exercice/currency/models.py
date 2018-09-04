# from django.conf import settings
from django.db import models
# from django.db.models.signals import pre_save, post_save, post_delete
# from django.dispatch import receiver

from python_exercice.models import BaseModel


class CurrencyRate(BaseModel):

    currency_name = models.CharField(max_length=3)
    currency_base_name = models.CharField(max_length=3)
    rate = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return '{} - {}: {}'.format(self.date, self.currency_name, self.rate)

    class Meta:
        ordering = ['-date', 'currency_name']
