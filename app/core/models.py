from django.db import models
import requests
from django.conf import settings
import json
from datetime import timedelta, datetime


class EntryManager(models.Manager):
    def retrieve_legacy(self, start_date, end_date=datetime.now().date()):
        """
        Loops through a date range, from the given start_date to today's date, and calls the .retrieve() method for each
        day (apart from weekends).
        :param start_date: a datetime.date() object to be used as the first date
        :param end_date: optional - the end date. Defaults to today's date.
        """
        try:
            assert start_date <= end_date
        except AssertionError:
            raise Exception('End date cannot be before start date')

        d = start_date
        delta = timedelta(days=1)

        while d <= end_date:
            if not d.weekday() in [5, 6]:
                self.retrieve(d.strftime("%Y-%m-%d"))
            d += delta

    def retrieve(self, date='latest'):
        """
        Retrieve and store exchange rate data from fixer.io

        :param date: optional date, to be provided in the format YYYY-MM-DD. If not provided, defaults to today's date
        """
        # call fixer.io
        response = requests.get('http://data.fixer.io/api/%s?access_key=%s' % (date, settings.FIXER_ACCESS_KEY))
        print(response)
        data = json.loads(response.content.decode())

        # only one entry can exist for each day. Start by checking for existing objects for today's date, and deleting
        # the rates for that day if one already exists
        entry, created = self.get_or_create(date=data['date'])

        if not created:
            entry.rates.all().delete()

        entry.base = data['base']
        entry.save()

        # bulk create exchange rate objects
        ExchangeRate.objects.bulk_create(
            [
                ExchangeRate(entry=entry, currency=currency, value=value) for currency, value in data['rates'].items()
            ]
        )


class Entry(models.Model):
    objects = EntryManager()
    base = models.CharField(max_length=3)
    date = models.DateField(unique=True)


class ExchangeRate(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='rates')
    currency = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=50, decimal_places=6)

    class Meta:
        unique_together = (
            'entry', 'currency'
        )

    def __str__(self):
        return '%s | %s>%s: %s' % (self.entry.date, self.entry.base, self.currency, self.value)
