import os

from typing import List

from data.session import Session
from data.fileset import FileSet
from data.models.filesetmodel import FileSetModel
from data.file import File
from data.models.filemodel import FileModel
from data.filecontentcache import FileContentCache
from logger import Logger

LOGGER = Logger()


class DataManager:
    def __init__(self) -> None:
        pass

    def createFileSet(self, fileSetPath: str) -> FileSet:
        LOGGER.info(f'DataManager.createFileset() fileSetPath={fileSetPath}')
        fileSetName = os.path.split(fileSetPath)[-1]
        with Session() as session:
            fileSetModel = FileSetModel(name=fileSetName, path=fileSetPath)
            session.add(fileSetModel)
            session.commit()
            fileSet = FileSet(model=fileSetModel)
            for fileName in os.listdir(fileSetPath):
                filePath = os.path.join(fileSetPath, fileName)
                fileModel = FileModel(name=fileName, path=filePath, fileSetModel=fileSetModel)
                session.add(fileModel)
                session.commit()
                file = File(model=fileModel)
                fileSet.addFile(file)
        return fileSet
    
    def fileSet(self, id: str) -> FileSet:
        LOGGER.info(f'DataManager.fileset() id={id}')
        with Session() as session:
            fileSetModel = session.get(FileSetModel, id)
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
        LOGGER.info(f'DataManager.updateFileset() fileSet={fileSet.name()}')
        with Session() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            if fileSetModel:
                fileSetModel.name = fileSet.name()
                session.commit()
                return fileSet
        return None
    
    def deleteFileSet(self, fileSet: FileSet) -> None:
        LOGGER.info(f'DataManager.deleteFileset() fileSet={fileSet.name()}')
        with Session() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            session.delete(fileSetModel)
            session.commit()
            cache = FileContentCache()
            for file in fileSet.files():
                cache.remove(file.id())

    def deleteAllFileSets(self) -> None:
        LOGGER.info(f'DataManager.deleteAllFileSets()')
        with Session() as session:
            cache = FileContentCache()
            fileSetModels = session.query(FileSetModel).all()
            for fileSetModel in fileSetModels:
                for fileModel in fileSetModel.fileModels:
                    cache.remove(fileModel.id)
                session.delete(fileSetModel)
            session.commit()