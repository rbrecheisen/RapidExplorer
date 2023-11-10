from PySide6.QtCore import QRunnable

from rapidx.app.data.db.db import Db
from rapidx.app.data.progresssignal import ProgressSignal


class Importer(QRunnable):
    def __init__(self, name: str, path: str, db: Db) -> None:
        super(Importer, self).__init__()
        self._name = name
        self._path = path
        self._db = db
        self._data = None
        self._signal = ProgressSignal()

    def name(self) -> str:
        return self._name

    def path(self) -> str:
        return self._path
    
    def db(self) -> Db:
        return self._db
    
    def data(self):
        return self._data
    
    def setData(self, data) -> None:
        self._data = data

    def signal(self) -> ProgressSignal:
        return self._signal
    
    def run(self) -> None:
        # self.signal().progress.emit(100)
        pass
