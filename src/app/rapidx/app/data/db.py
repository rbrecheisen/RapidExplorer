from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from rapidx.app.singleton import singleton
from rapidx.app.data.basemodel import BaseModel

DATABASE = 'db.sqlite3'
ECHO = False


@singleton
class Db:
    def __init__(self, engine=None):
        if not engine:
            engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
            BaseModel.metadata.create_all(engine)
        self._db = Session(engine)

    def __enter__(self):
        return self._db
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._db.close()