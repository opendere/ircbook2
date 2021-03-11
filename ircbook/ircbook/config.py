import functools
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


basedir = os.path.abspath(os.path.dirname(__file__))


@functools.lru_cache()
def get_engine():
    return create_engine('sqlite:////' + os.path.join(basedir, 'ircbook.sqlite'))


@functools.lru_cache()
def get_session():
    Session = sessionmaker()
    Session.configure(bind=get_engine())
    return Session()



# Create the SQLAlchemy db instance
#db = SQLAlchemy(app)

# Initialize Marshmallow
#ma = Marshmallow(app)
