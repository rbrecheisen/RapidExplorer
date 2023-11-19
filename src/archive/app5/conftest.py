import pytest

from sqlalchemy import create_engine

from rapidx.app.data.db.db import Db
from rapidx.app.data.basemodel import BaseModel

DATABASE = 'db.test.sqlite3'    # Memory database doesn't work because it gets cleared as soon as scope is lost
                                # which happens between threads
ECHO = False


@pytest.fixture(scope='function')
def db():    
    engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
    BaseModel.metadata.create_all(bind=engine)
    db = Db(engine)
    yield db
