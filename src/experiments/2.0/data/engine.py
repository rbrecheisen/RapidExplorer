import os

from sqlalchemy import create_engine

from singleton import singleton
from data.models.basemodel import BaseModel

DATABASE = os.environ.get('DATABASE', 'db.sqlite3')
DATABASEECHO = True if os.environ.get('DATABASEECHO', '0') =='1' else False


@singleton
class Engine:
    def __init__(self):
        self._engine = create_engine(f'sqlite:///{DATABASE}', echo=DATABASEECHO)
        BaseModel.metadata.create_all(self._engine)

    def get(self):
        return self._engine