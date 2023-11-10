from rapidx.app.data.db.db import Db
from rapidx.app.data.progresssignal import ProgressSignal


class Loader:
    def __init__(self, db: Db=None) -> None:
        self._db = db
        self._signal = ProgressSignal()

    def db(self) -> Db:
        return self._db

    def signal(self) -> ProgressSignal:
        return self._signal    
