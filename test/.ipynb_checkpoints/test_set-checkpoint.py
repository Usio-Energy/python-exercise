import pytest


@pytest.fixture
def fixer_caller():
    """An instance of the FixerApi
    """
    from ..api_handler import FixerApi
    from secrets import api_key
    
    return FixerApi(api_key=api_key)
    
    
@pytest.fixture
def tidy_data():
    return [OrderedDict([('base', 'EUR'),
                         ('date', datetime.date(2018, 9, 17)),
                         ('USD', 1.322891),
                         ('AUD', 1.278047),
                         ('CAD', 1.302303)]
                       )
           ]
    

def test_successfull_call(fixer_caller, api_key: str, **kwargs):
    """Sucessfull call test
    
    Parameters
    ----------
    fixer_caller: FixerApi
        api instance with the methods to be tested
    api_key: str
        key to the fixer.io 
    **kwargs:
        key word arguments to add to the call, usually start_date and end_date
    
    Returns
    -------
    None
    """
    assert fixer_caller.fixer_call(api_key, **kwargs).json()['success'] == True
    
def test_tidy_data(fixer_caller):
    """Tidy data test
    
    Parameters
    ----------
    fixer_caller: FixerApi
        api instance with the methods to be tested
    
    Returns
    -------
    None    
    """
    tidy_data = fixer_caller.make_tidy_data()
    assert all([~isinstance(value, dict) for item in tidy_data for value in item.values()])

def test_no_file_destruction(fixer_caller, tidy_data):
    """Testing that there is no destruction of data only aggregation
    
     Parameters
    ----------
    fixer_caller: FixerApi
        api instance with the methods to be tested
    
    tidy_data: List[OrderedDictionary]
        test data representing a the expected tidy data
    """
    file_name = os.path.join(os.path.join(os.getcwd(), 'data'), 'currencies.parquet')
    if os.path.isfile(file_name):
        old_data = pd.DataFrame(tidy_data).to_parquet(file_name)
        
        fixer_caller.save_tidy_data()
        
        new_data = pd.read_parquet(file_name)
        
        assert ~old_data.merge(new_data).empty