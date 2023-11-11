from sqlalchemy import create_engine

from singleton import singleton
from data.basemodel import BaseModel

DATABASE = 'db.sqlite3'
ECHO = False


@singleton
class Engine:
    def __init__(self, dbFile: str=None, echo=False):
        databaseFile = DATABASE
        echo = ECHO
        if dbFile:
            databaseFile = dbFile
            echo = echo
        self._engine = create_engine(f'sqlite:///{databaseFile}', echo=echo)
        BaseModel.metadata.create_all(self._engine)

    def get(self):
        return self._engine