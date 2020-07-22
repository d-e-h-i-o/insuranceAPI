from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base

engine = None
'''
db_session = scoped_session(lambda: sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
                                         '''
db_session = scoped_session(lambda: create_session(autocommit=False, bind=engine))

Base = declarative_base()
#Base.query = db_session.query_property()


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine


def init_db():
    from api_app import models
    Base.metadata.create_all(bind=engine)