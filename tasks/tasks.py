from celery.utils.log import get_task_logger
from . import celery, db
from .models import Rates
from .services import prepare_rates, store_rates, fetch_rates
from dateutil.relativedelta import relativedelta
from datetime import datetime

logger = get_task_logger(__name__)


@celery.task
def process_rates():
    """
    Fetching the exchange rates from a public API and store them in our database.
    More information on the REST API called here: https://fixer.io/documentation.
    """
    logger.info('Processing rates of the day {}...'.format(datetime.now()))
    rates_response = fetch_rates()
    rates = prepare_rates(rates_response.json()['rates'])
    store_rates(rates)
    logger.info('... Rates {} processed.'.format(rates.id))


@celery.task
def clean_rates(months=1):
    """
    Cleaning the rates stored in the database before a specified time in the past.
    n.b: The default is 1 month (asked in the task description).
    """
    logger.info('Deleting rates stored before last month....')
    datetime_remove_from = datetime.now() - relativedelta(months=months)
    delete_command = Rates.__table__.delete().where(Rates.inserted < datetime_remove_from)
    db.engine.execute(delete_command)
    logger.info('... Rates deleted.')
