from secrets import api_key

if name == "__main__":
    
    fixer_api = FixerApi(api_key, database_engine=False)
    
    fixer_api.fixer_call()
    fixer_api.make_tidy_data()
    fixer_api.save_tidy_data()