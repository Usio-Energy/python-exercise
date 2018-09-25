import logging
from datetime import datetime, timedelta
from currency_db_model import Currency
import json
import requests

class FixerObject(object):
    '''
    Store currency object
    '''
    def __init__(self, json_currency):
         # API settings
        self.date = json_currency['date']
        self.base = json_currency['base']
        self.rates = json.dumps(json_currency['rates'])

class Fixer(object):
    '''
    Retrieve currency, process amd injest into DB
    Ensure minimum one month storage of currency rates
    '''
    def __init__(self, api_url, key, base_currency, flasklog):
        self.base_url = api_url
        self.api_key= key
        self.base_currency = base_currency
        self.flasklog = flasklog
        
    def get_currency(self, date):
        '''
        Build-up API request
        '''
        date_string = date.strftime('%Y-%m-%d')
        url = f'{self.base_url}{date_string}?access_key={self.api_key}&base={self.base_currency}'
        request = requests.get(url)
        result = request.json()
        if result['success'] == False:
            self.flasklog(f'Bad request \n {result}')
        return FixerObject(result)

    def ensure_month_currency_history(self, db, date):
        '''
        Assume 30 days in a month for now
        '''
        self.flasklog('Checking one month of currency rates storage')
        month = [date - timedelta(x + 1) for x in range(30)]
        weekdays = []
        for date in month:
            if date.weekday() < 5:
                weekdays.append(date)
        for date in weekdays:
            fixerObject = self.get_currency(date)
            self.check_insert_date_currency(fixerObject, db)

    def check_insert_date_currency(self, fixerObject, db):
        '''
        Check db and update if record does not exist
        '''
        currency_for_date = db.query(Currency).filter(Currency.date==fixerObject.date and Currency.base==fixerObject.base).first()
        if currency_for_date is None:
            record = Currency(fixerObject.date, fixerObject.base, fixerObject.rates)
            db.add(record)
            self.flasklog(f'Added currency rates record into database for {fixerObject.date} and {fixerObject.base}')
        db.commit()