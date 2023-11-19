from sqlalchemy import create_engine

from singleton import singleton
from data.basemodel import BaseModel

DATABASE = 'db.sqlite3'
ECHO = False
TEST = False


@singleton
class Engine:
    def __init__(self):
        self._engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
        BaseModel.metadata.create_all(self._engine)

    def get(self):
        return self._engine