import os
import re

from typing import List

from PySide6.QtCore import QThreadPool

from data.progresssignal import ProgressSignal
from data.dbsession import DbSession
from data.file import File
from data.filemodel import FileModel
from data.fileset import FileSet
from data.filesetmodel import FileSetModel


class DataManager:
    def __init__(self) -> None:
        self._signal = ProgressSignal()

    def signal(self) -> ProgressSignal:
        return self._signal
    
    def loadFile(self, filePath: str) -> File:
        with DbSession() as session:
            fileModel = FileModel(path=filePath)
            session.add(fileModel)
            session.commit()
            file = File(fileModel=fileModel)
        return file
    
    def loadFileSet(self, fileSetPath: str, regex: str=r'.*') -> FileSet:
        with DbSession() as session:
            fileSetModel = FileSetModel(path=fileSetPath)
            session.add(fileSetModel)
            for fileName in os.listdir(fileSetPath):
                if re.match(regex, fileName):
                    filePath = os.path.join(fileSetPath, fileName)
                    fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
                    session.add(fileModel)
            session.commit()
            fileSet = FileSet(fileSetModel=fileSetModel)
        return fileSet
    
    def updateFileSetName(self, id: str, name: str) -> None:
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, id)
            fileSetModel.name = name
            session.commit()

    # def data(self) -> RegisteredMultiFileSetModel:
    #     if self._importer:
    #         return self._importer.data()
    #     return None
    
    # def printFileCache(self) -> None:
    #     FileCache().printFiles()

    # # Deleting data

    # def deleteData(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> None:
    #     cache = FileCache()
    #     cache.removeMultiFileSet(registeredMultiFileSetModel)
    #     with DbSession() as session:
    #         model = session.get(MultiFileSetModel, registeredMultiFileSetModel.id)
    #         session.delete(model)
    #         session.commit()

    # def deleteAllData(self) -> None:
    #     cache = FileCache()
    #     cache.removeAllData()
    #     with DbSession() as session:
    #         models = session.query(MultiFileSetModel).all()
    #         for model in models:
    #             session.delete(model)
    #         session.commit()

    # # Loading models

    # def loadModels(self) -> None:
    #     modelLoader = RegisteredMultiFileSetModelLoader()
    #     registeredMultiFileSetModels = modelLoader.loadAll()
    #     multiFileSetLoaded = True
    #     for registeredMultiFileSetModel in registeredMultiFileSetModels:          
    #         for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
    #             fileSetLoaded = True
    #             for registeredFileModel in registeredFileSetModel.registeredFileModels:
    #                 if self._fileInCache(registeredFileModel):
    #                     registeredFileModel.loaded = True
    #                 else:
    #                     # If there is one file model that is not loaded, the whole fileset is not loaded
    #                     registeredFileModel.loaded = False
    #                     fileSetLoaded = False
    #             registeredFileSetModel.loaded = fileSetLoaded
    #             if not fileSetLoaded:
    #                 multiFileSetLoaded = False
    #         registeredMultiFileSetModel.loaded = multiFileSetLoaded
    #     return registeredMultiFileSetModels

    # def _fileInCache(self, registeredFileModel: RegisteredFileModel) -> bool:
    #     cache = FileCache()
    #     if not cache.has(registeredFileModel.id):
    #         return False
    #     return True
    
    # # Importing data

    # def importFile(self, filePath: str, fileType: FileType) -> None:
    #     self._importer = None
    #     self._importer = FileImporter(path=filePath, fileType=fileType)
    #     self._importer.signal().progress.connect(self._updateImportProgress)
    #     QThreadPool.globalInstance().start(self._importer)

    # def importFileSet(self, dirPath: str, fileType: FileType) -> None:
    #     self._importer = None
    #     self._importer = FileSetImporter(path=dirPath, fileType=fileType)
    #     self._importer.signal().progress.connect(self._updateImportProgress)
    #     QThreadPool.globalInstance().start(self._importer)

    # def importMultiFileSet(self, dirPath: str, fileType: FileType) -> None:
    #     self._importer = None
    #     self._importer = MultiFileSetImporter(path=dirPath, fileType=fileType)
    #     self._importer.signal().progress.connect(self._updateImportProgress)
    #     QThreadPool.globalInstance().start(self._importer)

    # def _updateImportProgress(self, progress) -> None:
    #     self._signal.progress.emit(progress)

    # # Loading data

    # def loadRegisteredMultiFileSetModel(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> None:
    #     loader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel)
    #     loader.signal().progress.connect(self._updateLoadProgress)
    #     loader.execute()

    # def _updateLoadProgress(self, progress) -> None:
    #     self._signal.progress.emit(progress)

    # # Getting data

    # def getFileFromCache(self, id: str) -> File:
    #     return FileCache().get(id)
    
    # def getRegisteredMultiFileSetModels(self) -> List[RegisteredMultiFileSetModel]:
    #     registeredMultiFileSetModels = []
    #     with DbSession() as session:
    #         multiFileSetModels = session.query(MultiFileSetModel).all()
    #         for multiFileSetModel in multiFileSetModels:
    #             loader = RegisteredMultiFileSetModelLoader()
    #             registeredMultiFileSetModels.append(loader.load(multiFileSetModel.id))
    #     return registeredMultiFileSetModels
    
    # def getRegisteredMultiFileSetModelByName(self, name) -> RegisteredMultiFileSetModel:
    #     registeredMultiFileSetModel = None
    #     with DbSession() as session:
    #         multiFileSetModel = session.query(MultiFileSetModel).filter_by(name=name).one()
    #         loader = RegisteredMultiFileSetModelLoader()
    #         registeredMultiFileSetModel = loader.load(multiFileSetModel.id)
    #     return registeredMultiFileSetModel

    # # Updating names

    # def updateFileSetName(self, id: str, name: str) -> None:
    #     with DbSession() as session:
    #         fileSetModel = session.get(FileSetModel, id)
    #         fileSetModel.name = name
    #         session.commit()

    # def updateMultiFileSetName(self, id: str, name: str) -> None:
    #     with DbSession() as session:
    #         multiFileSetModel = session.get(MultiFileSetModel, id)
    #         multiFileSetModel.name = name
    #         session.commit()
