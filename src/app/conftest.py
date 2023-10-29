import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from rapidx.app.data.db import Db
from rapidx.app.data.basemodel import BaseModel


@pytest.fixture(scope='function')
def db():    
    engine = create_engine('sqlite:///:memory:', echo=False)
    BaseModel.metadata.create_all(bind=engine)
    # session = Session(engine)
    db = Db(engine)
    yield db
    db.close()