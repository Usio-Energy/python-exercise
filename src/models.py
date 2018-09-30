from sqlalchemy import (Column,
                        Date,
                        DECIMAL,
                        ForeignKey,
                        Integer,
                        Sequence,
                        String,
                        UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, Sequence('currency_id_seq'), primary_key=True)
    code = Column(String, unique=True, nullable=False)


class Batch(Base):
    __tablename__ = 'batch'
    id = Column(Integer, Sequence('batch_id_seq'), primary_key=True)
    date = Column(Date, unique=True, nullable=False)
    base_currency_id = Column(Integer, ForeignKey('currency.id'),
                              nullable=False)
    base_currency = relationship('Currency', backref=backref('batches'))


class CurrencyRate(Base):
    __tablename__ = 'currency_rate'
    id = Column(Integer, Sequence('currency_rate_id_seq'), primary_key=True)
    rate = Column(DECIMAL, nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False)
    currency = relationship('Currency', backref=backref('currency_rates'))
    batch_id = Column(Integer, ForeignKey('batch.id'), nullable=False)
    batch = relationship('Batch', backref=backref('currency_rates'))
    __table_args__ = (UniqueConstraint('currency_id', 'batch_id',
                                       name='_currency_batch_uc'), )
