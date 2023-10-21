import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rapidx.app.basemodel import BaseModel


@pytest.fixture(scope='function')
def session():
    print('Creating test database...')
    engine = create_engine('sqlite:///:memory:')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()