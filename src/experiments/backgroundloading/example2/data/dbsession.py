import os

from sqlalchemy.orm import sessionmaker
import os

from data import engine
from data.engine import Engine


class DbSession:
    def __init__(self) -> None:
        Session = sessionmaker(bind=Engine().get())
        self._session = Session()

    def __enter__(self):
        return self._session
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()
