from abc import ABC, abstractmethod
from PySide6.QtCore import QRunnable
from signals.loaderprogresssignal import LoaderProgressSignal


class Loader(QRunnable, ABC):
    def __init__(self, path: str) -> None:
        super(Loader, self).__init__()
        self._path = path
        self._signal = LoaderProgressSignal()

    def path(self) -> str:
        return self._path
    
    def signal(self) -> LoaderProgressSignal:
        return self._signal
    
    @abstractmethod
    def data(self):
        pass
    
    @abstractmethod
    def run(self):
        pass