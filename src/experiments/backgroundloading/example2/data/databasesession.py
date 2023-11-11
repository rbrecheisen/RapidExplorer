from sqlalchemy.orm import Session, sessionmaker

from data.engine import Engine


class DatabaseSession:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def engine(self):
        return self._engine

    def get(self):
        return self._session