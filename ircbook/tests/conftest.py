import pytest
from sqlalchemy import create_engine
from ircbook.models import Base


engine = create_engine('sqlite://')  # in memory engine


@pytest.fixture(autouse=True, scope='function')
def mock_db_session(mocker):
    mocker.patch('ircbook.config.get_engine', lambda: engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
