from sqlalchemy.orm import Session
from PySide6.QtCore import QRunnable

from rapidx.tests.data.progresssignal import ProgressSignal


class Importer(QRunnable):
    def __init__(self, path: str, session: Session) -> None:
        self._path = path
        self._session = session
        self._data = None
        self._signal = ProgressSignal()

    def path(self) -> str:
        return self._path
    
    def session(self) -> Session:
        return self._session
    
    def data(self):
        return self._data
    
    def setData(self, data) -> None:
        self._data = data

    def signal(self) -> ProgressSignal:
        return self._signal
    
    def execute(self) -> None:
        raise RuntimeError('Method must be overridden in derived class')