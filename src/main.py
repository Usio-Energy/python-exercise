import datetime
import logging
import os
import requests

from exceptions import InvalidResponseCodeException, MissingEnvVarException
from models import Batch, Currency, CurrencyRate
from utils import create_session

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_or_create_currency_instances(currency_codes, session):
    currency_code_set = set(currency_codes)
    existing_codes = list(session.query(Currency)
                          .filter(Currency.code.in_(currency_code_set))
                          .values('code'))
    # query.values returns a list of tuples, so we have to translate this to a
    # flat set of strings
    existing_code_set = {existing_code_tuple[0]
                         for existing_code_tuple in existing_codes}
    currencies_codes_not_in_db = (currency_code_set
                                  - existing_code_set)
    session.bulk_save_objects(
        [Currency(code=code) for code in currencies_codes_not_in_db])
    return session.query(Currency)\
        .filter(Currency.code.in_(currency_code_set)).all()


def save_batch(date_str, base_currency, session):
    year, month, day = [int(item) for item in date_str.split('-')]
    date = datetime.date(year=year, month=month, day=day)
    batch = Batch(date=date, base_currency=base_currency)
    session.add(batch)
    return batch


def save_rates(rates_dict, batch, currency_code_inst_dict, session):
    currency_rates = []
    for currency_code, rate in rates_dict.items():
        currency_rates.append(
            CurrencyRate(
                batch=batch,
                currency=currency_code_inst_dict[currency_code],
                rate=rate)
        )
    session.add_all(currency_rates)
    return currency_rates


def save_fixer_data_to_db(fixer_dict):
    logging.info('saving batch to db')
    session = create_session()
    try:
        # First we want to get or create the relevant currency instances
        base_currency_code = fixer_dict['base']
        rates_dict = fixer_dict['rates']
        returned_currency_codes = list(rates_dict.keys())
        returned_currency_codes.append(base_currency_code)
        currency_instances = get_or_create_currency_instances(
            currency_codes=returned_currency_codes, session=session)
        currency_code_inst_dict = {inst.code: inst for inst in
                                   currency_instances}

        # once we have our currency instances we need to create a new batch,
        # foreign keying to the base currency
        base_currency_inst = currency_code_inst_dict[base_currency_code]
        batch = save_batch(date_str=fixer_dict['date'],
                           base_currency=base_currency_inst,
                           session=session)

        # now save the rates we received from the api
        num_rates = save_rates(rates_dict=rates_dict,
                               currency_code_inst_dict=currency_code_inst_dict,
                               batch=batch, session=session)

        logging.info('successfully saved {} currency rates'.format(num_rates))
        session.transaction.commit()
    except Exception as err:
        session.rollback()
        session.close()
        logging.exception('could not process batch due to err: {}'.format(err))
        # re raise the exception after catching and logging
        raise
    finally:
        # close the session regardless of what happens
        session.close()


def get_fixer_data(api_key, url, base_currency):
    logging.info('sending request for currency data to {}'.format(url))
    response = requests.get(url=url, params={'access_key': api_key,
                                             'base': base_currency})
    if not response.ok or response.json()['success'] is not True:
        msg = 'recieved status {} from src url {}' \
            .format(response.status_code, url)
        logger.exception(msg)
        raise InvalidResponseCodeException(msg)
    return response.json()


def handler(event, context):
    """
    handler function compatible AWS lambda function
    """
    logger.info('script start')
    fixer_api_key = os.environ.get('FIXER_API_KEY')
    fixer_url = os.environ.get('FIXER_URL')
    base_currency = os.environ.get('FIXER_BASE_CURRENCY', 'EUR')
    if fixer_api_key is None:
        msg = 'api key environment variable not set!'
        logger.error(msg)
        raise MissingEnvVarException(msg)
    elif fixer_url is None:
        msg = 'url environment variable not set!'
        logger.error(msg)
        raise MissingEnvVarException(msg)
    fixer_json_data = get_fixer_data(api_key=fixer_api_key,
                                     url=fixer_url,
                                     base_currency=base_currency)
    save_fixer_data_to_db(fixer_json_data)
    logger.info('script end')


if __name__ == '__main__':
    handler(None, None)

