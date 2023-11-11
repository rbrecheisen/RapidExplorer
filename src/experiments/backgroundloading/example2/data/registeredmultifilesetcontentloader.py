from PySide6.QtCore import QRunnable

from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.progresssignal import ProgressSignal
from data.filecache import FileCache
from data.filetype import FileType


class RegisteredMultiFileSetContentLoader(QRunnable):
    def __init__(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel, fileType: FileType) -> None:
        super(RegisteredMultiFileSetContentLoader, self).__init__()
        self._registeredMultiFileSetModel = registeredMultiFileSetModel
        self._nrFiles = self._registeredMultiFileSetModel.nrFiles()
        self._fileType = fileType
        self._signal = ProgressSignal()

    def data(self) -> RegisteredMultiFileSetModel:
        return self._registeredMultiFileSetModel

    def signal(self) -> ProgressSignal:
        return self._signal

    def run(self):
        i = 0
        cache = FileCache()
        for registeredFileSetModel in self._registeredMultiFileSetModel.registeredFileSetModels:
            for registeredFileModel in registeredFileSetModel.registeredFileModels:
                file = self._fileType.read(registeredFileModel)
                cache.add(file)
                progress = int((i + 1) / self._nrFiles * 100)
                self._signal.progress.emit(progress)
                print('.', end='', flush=True)
                i += 1