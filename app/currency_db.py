from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sql_config_uri = {
    'development': 'sqlite:////tmp/Development.db',
    'testing': 'sqlite:////tmp/Testing.db',
    'production': 'sqlite:////tmp/Production.db'
}

engine = create_engine(sql_config_uri['development'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit = False,
                                        autoflush = False,
                                        bind = engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import currency_db_model
    Base.metadata.create_all(bind = engine)


