from sqlalchemy.orm import sessionmaker

from mosamaticdesktop.data.engine import Engine


class Session:
    def __init__(self) -> None:
        session = sessionmaker(bind=Engine().get())
        self._session = session()

    def __enter__(self):
        return self._session
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()
