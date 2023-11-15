from PySide6.QtCore import QThreadPool

from data.progresssignal import ProgressSignal
from data.dbsession import DbSession
from data.filecache import FileCache
from data.filetype import FileType
from data.fileimporter import FileImporter
from data.filesetimporter import FileSetImporter
from data.multifilesetimporter import MultiFileSetImporter
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader


class DatabaseManager:
    def __init__(self) -> None:
        self._signal = ProgressSignal()
        self._importer = None
        self._fileSetImporter = None
        self._multiFileSetImporter = None

    def signal(self) -> ProgressSignal:
        return self._signal
    
    def data(self) -> RegisteredMultiFileSetModel:
        if self._importer:
            return self._importer.data()
        return None
    
    def printFileCache(self) -> None:
        FileCache().printFiles()

    def deleteData(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> None:
        cache = FileCache()
        cache.removeMultiFileSet(registeredMultiFileSetModel)
        with DbSession() as session:
            model = session.get(MultiFileSetModel, registeredMultiFileSetModel.id)
            session.delete(model)
            session.commit()

    def deleteAllData(self) -> None:
        cache = FileCache()
        cache.removeAllData()
        with DbSession() as session:
            models = session.query(MultiFileSetModel).all()
            for model in models:
                session.delete(model)
            session.commit()

    def loadModels(self) -> None:
        modelLoader = RegisteredMultiFileSetModelLoader()
        registeredMultiFileSetModels = modelLoader.loadAll()
        for registeredMultiFileSetModel in registeredMultiFileSetModels:            
            if self._fileInCache(registeredMultiFileSetModel):
                registeredMultiFileSetModel.loaded = True
                # self.addRegisteredMultiFileSetModel(registeredMultiFileSetModel, loaded=True)
            else:
                registeredMultiFileSetModel.loaded = False
                # self.addRegisteredMultiFileSetModel(registeredMultiFileSetModel, loaded=False)
        return registeredMultiFileSetModels

    def _fileInCache(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> bool:
        cache = FileCache()
        for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
            for registeredFileModel in registeredFileSetModel.registeredFileModels:
                if not cache.has(registeredFileModel.id):
                    return False
        return True

    def importFile(self, filePath: str, fileType: FileType) -> None:
        self._importer = None
        self._importer = FileImporter(path=filePath, fileType=fileType)
        self._importer.signal().progress.connect(self._updateProgress)
        QThreadPool.globalInstance().start(self._importer)

    def importFileSet(self, dirPath: str, fileType: FileType) -> None:
        self._importer = None
        self._importer = FileSetImporter(path=dirPath, fileType=fileType)
        self._importer.signal().progress.connect(self._updateProgress)
        QThreadPool.globalInstance().start(self._importer)

    def importMultiFileSet(self, dirPath: str, fileType: FileType) -> None:
        self._importer = None
        self._importer = MultiFileSetImporter(path=dirPath, fileType=fileType)
        self._importer.signal().progress.connect(self._updateProgress)
        QThreadPool.globalInstance().start(self._importer)

    def _updateProgress(self, progress) -> None:
        self._signal.progress.emit(progress)
