import os, inspect, sys, unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
baseDir = os.path.join(parentDir, "app")
sys.path.insert(0, baseDir)
from fixer import Fixer, FixerObject

class BasicsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        engine = create_engine('sqlite:////tmp/test4.db', convert_unicode=True)
        self.db = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))
        self.Base = declarative_base()
        self.Base.query = self.db.query_property()
        class Currency(self.Base):
            __tablename__ = 'Currency'
            id = Column(Integer, primary_key=True)
            date = Column(String(10))
            base = Column(String(3))
            rates = Column(String)

            def __init__(self, date, base, rates):
                self.date = date
                self.base = base
                self.rates = rates
        self.Base.metadata.create_all(bind = engine)
        self.Currency = Currency
        self.fixer_object = Fixer('','','')
        self.db.query(self.Currency).delete()
    
    @classmethod
    def tearDownClass(self):
        self.db.query(self.Currency).delete()

    def test_a_check_insert_date_currency_one_entry_value(self):
        '''
        insert first entry into db and check the values 
        '''
        query = {
            "base":"EUR",
            "date":"2018-09-22",
            "rates":{
            "AED":4.32298,
            "AFN":89.239799
            }
        }    
        self.db.query(self.Currency).delete()
        fixer_query = FixerObject(query)
        self.fixer_object.check_insert_date_currency(fixer_query, self.db)
        self.assertTrue(self.db.query(self.Currency).first().date == query["date"])

    def test_b_check_insert_date_currency_two_entries(self):
        '''
        insert second entry into db and check the total number of records (2)
        '''
        query = {
            "base":"EUR",
            "date":"2018-09-20",
            "rates":{
            "AED":4.32298,
            "AFN":89.239799
            }
        }    
        fixer_query = FixerObject(query)
        self.fixer_object.check_insert_date_currency(fixer_query, self.db)
        self.assertTrue(self.db.query(self.Currency).count() == 2)

    def test_c_check_insert_date_currency_exisiting_entry(self):
        '''
        try to insert third duplicate entry into db and check the total number of records (2)
        '''
        query = {
            "base":"EUR",
            "date":"2018-09-20",
            "rates":{
            "AED":4.32298,
            "AFN":89.239799
            }
        }    
        fixer_query = FixerObject(query)
        self.fixer_object.check_insert_date_currency(fixer_query, self.db)
        self.assertTrue(self.db.query(self.Currency).count() == 2)

if __name__ == '__main__':
    unittest.main()