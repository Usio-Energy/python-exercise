from flask import Flask
from fixer import Fixer
from celeryapp import make_celery
from currency_db import init_db, db_session
from currency_db_model import Currency
from datetime import date, datetime
from config import config
import logging
import logging.handlers

app = Flask(__name__)
config_name = 'development' 
app.config.from_object(config[config_name])
handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.info("Initializing server")
fixer = Fixer(api_url = 'http://data.fixer.io/api/',  \
            key = '945665349f11c11734fe2f34da243516', \
            base_currency = 'EUR', flasklog = app.logger.info)
init_db()            
celery = make_celery(app)

@celery.task(queue='try')
def update_currency(fixer, db_session, logger):
    logger("Updating currency")
    dt = date.today()
    dt = datetime(dt.year, dt.month, dt.day)
    fixer.ensure_month_currency_history(db_session, dt)
    logger("Adding current date currency")
    fixerObject = fixer.get_currency(dt)
    fixer.check_insert_date_currency(fixerObject, db_session)

update_currency(fixer, db_session, app.logger.info)

@app.route('/get_currency')
def get_currency():
    '''
    check db from server
    '''
    return ''.join(Currency.query.all())

if __name__ == '__main__':
    app.run()