from collections import OrderedDict
import datetime
import os
import pandas as pd
import requests

from typing import List


class FixerApi:
    
    """Fixer api caller 
    
    This calls calls, cleans and saves the data from the Fixer Currency Rates API
    
    """
    
    def __init__(api_key, database_engine=None):
        self.api_key = api_key
        get_past_month=False
        
        if not database_engine:
            self.engine = None
            self.storage_location = os.path.join(os.getcwd(), 'data')
            
            if not os.isdir(self.storage_location):
                os.makedirs(self.storage_location)
                get_past_month=True
                
        else:
            self.engine = database_engine
        
        self.response
        self.tidy_data
        
    def fixer_call(start_date: str=None, end_date: str=None, get_past_month: bool=False) -> dict:
        """Calling the fixer api and collecting currency data 

        The data collected corresponds to the last day or to the last month as required

        Parameters
        ----------

        api_key: str
            key to the fixer.io 
        start_date: str, optional
            YYYY-MM-DD stating the starting date from which to collect data. For time series only.
        end_date: str, optional
            YYYY-MM-DD end date up to when to collect data. For time series only.

        Returns
        -------
        dict
            Json parsed dictionary containing the currency rates and metadata
        """
        if start_date or end_date or get_past_month:
            if not end_date:
                end_date = str(dt.date.today())
            if not start_date:
                start_date = str(dt.date.today().replace(month=dt.date.today().month -1))
            query = f'http://data.fixer.io/api/timeseries?access_key={self.api_key}&start_date={start_date}&end_date={end_date}'
        else:
            query = f'http://data.fixer.io/api/latest?access_key={self.api_key}'
        
        self.response = requests.get(query).json()
        return self.response

    def make_tidy_data() -> List[OrderedDict]:
        """Transfomind a nested dictionary call into tidy data to store in the database 

        This function is agnostic if the call is a single date or a time series.

        Parameters
        ----------
        response: dict
            Dictionary containing the json parsed response from fixer.io

        Returns
        -------
        List[OrderedDict]
            Flat dictionary containing Date, TimeStamp, BaseCurrency and CurrencyRates for a given call
        """
        tidy_dict_coll = []

        if 'timeseries' in self.response.keys(): 
            for key, values in self.response['rates'].items():
                if dt.datetime.strptime(key, "%Y-%m-%d").date().isoweekday() not in [6, 7]:
                    tidy_dict_coll.append(OrderedDict({'base': self.response['base'], 
                                                       'date': dt.datetime.strptime(key, "%Y-%m-%d").date(), 
                                                       **values
                                                      }
                                                     )
                                         )
        else:
            tidy_dict = OrderedDict({key: value if key != 'date' else dt.datetime.strptime(value, "%Y-%m-%d").date()
                                     for key, value in self.response.items() 
                                     if not isinstance(value, dict) 
                                     and key != 'success' 
                                     and (key == 'date' 
                                          and dt.datetime.strptime(value, "%Y-%m-%d").date().isoweekday() 
                                          not in [6, 7]
                                         )
                                    }
                                   )
            tidy_dict.update(**self.response['rates'])
            tidy_dict_coll = [tidy_dict]

        self.tidy_data = tidy_dict_coll
        return self.tidy_data
    
    def save_tidy_data():
        """Saving the clean data into the database or pickle file
        
        Depending if we have set up a database or not the class saves the data
        in the corresponding format. 
        
        I used pandas as a data handler it provides capabilities to store the data in
        a database or in a file, although it adds a lot of overhead.
        
        Pandas is also useful to check for completion in the long term as we can 
        easily obtain the required date range and compare it agains the data in 
        both the storage and the api call. 
        
        """
        if self.engine:
            pd.DataFrame(self.tidy_data).to_sql(con=self.engine)
        else:
            file_name = os.path.join(self.storage_location, 'currencies.parquet')
            if not os.path.join(file_name):
                pd.DataFrame(self.tidy_data).to_parquet(file_name)
            else:
                currencies = (pd.read_parquet(file_name)
                              .append(pd.DataFrame(self.tidy_data))
                              .drop_duplicates()
                              .set_index('date')
                             )
                
                if self.is_complete(currencies):
                    currencies.reset_index().to_parquet(file_name)
                else:
                    self.fixer_call(get_past_month_weekdays=True)
                    self.make_tidy_call()
                    pd.DataFrame(self.tidy_data).to_parquet(file_name)
    
    @staticmethod
    def is_complete(currencies):
        complete_dates = (pd.DataFrame(currencies).astype({'date': 'datetime64[ns]'})
                                  .merge(get_past_month_weekdays(),
                                         how='right'
                                        )
                                 )
        return complete_dates.size == complete_dates.dropna().size
    
    @staticmethod
    def get_past_month_weekdays():
        return (pd.date_range(start=dt.datetime.today().date().replace(month=dt.date.today().month -1),
                              end=dt.datetime.today(), freq=BDay()
                             )
                .rename('date').to_frame().reset_index(drop=True)
               )