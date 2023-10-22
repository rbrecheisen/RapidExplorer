import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from rapidx.tests.data.basemodel import BaseModel


@pytest.fixture(scope='function')
def session():
    engine = create_engine('sqlite:///:memory:')
    BaseModel.metadata.create_all(bind=engine)
    session = Session(engine)
    yield session
    session.close()