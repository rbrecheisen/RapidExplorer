from PySide6.QtCore import QRunnable

from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.progresssignal import ProgressSignal
from data.filetype import FileType


class Importer(QRunnable):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(Importer, self).__init__()
        self._path = path
        self._fileType = fileType
        self._registeredMultiFileSetModel = None
        self._signal = ProgressSignal()

    def path(self) -> str:
        return self._path
    
    def fileType(self) -> FileType:
        return self._fileType
    
    def data(self) -> RegisteredMultiFileSetModel:
        return self._registeredMultiFileSetModel
    
    def setData(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel):
        self._registeredMultiFileSetModel = registeredMultiFileSetModel

    def signal(self) -> ProgressSignal:
        return self._signal

    def run(self):
        raise NotImplementedError('Not implemented')