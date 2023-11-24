from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.progresssignal import ProgressSignal
from data.filecache import FileCache
from data.filetypefactory import FileTypeFactory


class RegisteredMultiFileSetContentLoader:
    def __init__(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> None:
        super(RegisteredMultiFileSetContentLoader, self).__init__()
        self._registeredMultiFileSetModel = registeredMultiFileSetModel
        self._nrFiles = self._registeredMultiFileSetModel.nrFiles()
        self._signal = ProgressSignal()

    def signal(self) -> ProgressSignal:
        return self._signal

    def execute(self) -> RegisteredMultiFileSetModel:
        i = 0
        cache = FileCache()
        self._registeredMultiFileSetModel.loaded = False
        for registeredFileSetModel in self._registeredMultiFileSetModel.registeredFileSetModels:
            for registeredFileModel in registeredFileSetModel.registeredFileModels:
                if not cache.has(registeredFileModel.id):
                    fileType = FileTypeFactory.forName(registeredFileModel.fileType)
                    if fileType.check(registeredFileModel.path):
                        file = fileType.read(registeredFileModel)
                        registeredFileModel.loaded = True
                        cache.add(file)
                        progress = int((i + 1) / self._nrFiles * 100)
                        self._signal.progress.emit(progress)
                        print('.', end='', flush=True)
                        i += 1
                else:
                    print(f'File {registeredFileModel.path} already in cache (skipping)')
                registeredFileModel.loaded = True
            registeredFileSetModel.loaded = True
        self._registeredMultiFileSetModel.loaded = True
        return self._registeredMultiFileSetModel