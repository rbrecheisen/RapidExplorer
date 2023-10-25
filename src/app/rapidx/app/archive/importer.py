from abc import ABC, abstractmethod
from PySide6.QtCore import QRunnable

from rapidx.app.importerprogresssignal import ImporterProgressSignal


class Importer(QRunnable, ABC):
    def __init__(self, path: str=None) -> None:
        super(Importer, self).__init__()
        self._path = path
        self._signal = ImporterProgressSignal()

    def path(self) -> str:
        return self._path
    
    def signal(self) -> ImporterProgressSignal:
        return self._signal
    
    @abstractmethod
    def data(self):
        pass
    
    @abstractmethod
    def run(self):
        pass