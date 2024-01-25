import os

from typing import List

from PySide6.QtCore import QObject, Signal

from mosamaticdesktop.data.session import Session
from mosamaticdesktop.data.fileset import FileSet
from mosamaticdesktop.data.models.filesetmodel import FileSetModel
from mosamaticdesktop.data.file import File
from mosamaticdesktop.data.models.filemodel import FileModel
from mosamaticdesktop.data.filecontentcache import FileContentCache
from mosamaticdesktop.singleton import singleton
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


@singleton
class DataManager:
    class DataManagerUpdatedSignal(QObject):
        updated = Signal(bool)

    def __init__(self) -> None:
        self._signal = self.DataManagerUpdatedSignal()

    def signal(self):
        return self._signal

    def createFile(self, filePath: str) -> FileSet:
        with Session() as session:
            fileSetPath = os.path.split(filePath)[0]
            fileSetName = fileSetPath.split(os.path.sep)[-1]
            fileSetModel = FileSetModel(name=fileSetName, path=fileSetPath)
            session.add(fileSetModel)
            fileName = os.path.split(filePath)[1]
            fileModel = FileModel(name=fileName, path=filePath, fileSetModel=fileSetModel)
            session.add(fileModel)
            session.commit()
            fileSet = FileSet(model=fileSetModel)
        self._signal.updated.emit(True)
        return fileSet


    def createFileSet(self, fileSetPath: str) -> FileSet:
        fileSetName = os.path.split(fileSetPath)[-1]
        with Session() as session:
            fileSetModel = FileSetModel(name=fileSetName, path=fileSetPath)
            session.add(fileSetModel)
            session.commit()
            fileSet = FileSet(model=fileSetModel)
            nrFiles = 0
            for fileName in os.listdir(fileSetPath):
                if fileName.startswith('.'):
                    continue
                filePath = os.path.join(fileSetPath, fileName)
                fileModel = FileModel(name=fileName, path=filePath, fileSetModel=fileSetModel)
                session.add(fileModel)
                session.commit()
                file = File(model=fileModel)
                fileSet.addFile(file)
                nrFiles += 1
        self._signal.updated.emit(True)
        return fileSet
    
    def fileSet(self, id: str) -> FileSet:
        with Session() as session:
            fileSetModel = session.get(FileSetModel, id)
            if fileSetModel:
                fileSet = FileSet(model=fileSetModel)
                return fileSet
        return None
    
    def fileSetByName(self, name: str) -> FileSet:
        with Session() as session:
            fileSetModel = session.query(FileSetModel).filter_by(name=name).one()
            if fileSetModel:
                fileSet = FileSet(model=fileSetModel)
                return fileSet
        return None
    
    def fileSets(self) -> List[FileSet]:
        with Session() as session:
            fileSetModels = session.query(FileSetModel).all()
            fileSets = []
            for fileSetModel in fileSetModels:
                fileSet = FileSet(model=fileSetModel)
                fileSets.append(fileSet)
        return fileSets

    def updateFileSet(self, fileSet: FileSet) -> FileSet:
        with Session() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            if fileSetModel:
                fileSetModel.name = fileSet.name()
                session.commit()
                return FileSet(model=fileSetModel)
        self._signal.updated.emit(True)
        return None
    
    def deleteFileSet(self, fileSet: FileSet) -> None:
        with Session() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            session.delete(fileSetModel)
            session.commit()
            cache = FileContentCache()
            for file in fileSet.files():
                cache.remove(file.id())
        self._signal.updated.emit(True)

    def deleteAllFileSets(self) -> None:
        with Session() as session:
            cache = FileContentCache()
            fileSetModels = session.query(FileSetModel).all()
            for fileSetModel in fileSetModels:
                for fileModel in fileSetModel.fileModels:
                    cache.remove(fileModel.id)
                session.delete(fileSetModel)
            session.commit()
        self._signal.updated.emit(True)
