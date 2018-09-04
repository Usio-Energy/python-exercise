from datetime import date, timedelta

from django.core.management.base import BaseCommand

from python_exercice.currency.tasks import store_currency_rate


class Command(BaseCommand):
    help = 'Collect the currency rates for the last 31 days'

    def handle(self, *args, **options):
        for delta in range(0,32):
            tmp_date = date.today() - timedelta(delta)
            # Don't collect rates for weekend
            if tmp_date.strftime('%w') not in ['0', '6']:
                tmp_date_formatted = tmp_date.strftime('%Y-%m-%d')
                store_currency_rate(tmp_date)
                print('Collecting rates for {}'.format(tmp_date))
