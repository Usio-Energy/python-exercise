from currency_db import Base
from sqlalchemy import Column, Integer, String

class Currency(Base):
    __tablename__ = 'Currency'
    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    base = Column(String(3))
    rates = Column(String)

    def __init__(self, date, base, rates):
        self.date = date
        self.base = base
        self.rates = rates
        


