import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from rapidx.app.data.db.db import Db
from rapidx.app.data.basemodel import BaseModel

DATABASE = 'db-test.sqlite3'
ECHO = False


@pytest.fixture(scope='function')
def db():    
    engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
    BaseModel.metadata.create_all(bind=engine)
    # session = Session(engine)
    db = Db(engine)
    yield db
    # db.close()