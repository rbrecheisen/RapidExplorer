import os

from typing import List

from PySide6.QtCore import QSettings

from data.datamanagersignal import DataManagerSigal
from data.dbsession import DbSession
from data.objectcache import ObjectCache
from data.filemodel import FileModel
from data.fileset import FileSet
from data.filesetmodel import FileSetModel
from data.filetype import FileType
from data.allfiletype import AllFileType
from utils import SettingsIniFile
from logger import Logger

LOGGER = Logger()


class DataManager:
    def __init__(self) -> None:
        self._settings = QSettings(SettingsIniFile().path(), QSettings.Format.IniFormat)
        self._signal = DataManagerSigal()

    def settings(self) -> QSettings:
        return self._settings
    
    def signal(self) -> DataManagerSigal:
        return self._signal
    
    # GET
    
    def fileSet(self, id: str) -> FileSet:
        LOGGER.info(f'DataManager.fileSet() id={id}')
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, id)
            fileSet = FileSet(fileSetModel=fileSetModel)
        return fileSet
    
    def fileSetByName(self, name: str) -> FileSet:
        LOGGER.info(f'DataManager.fileSetByName() name={name}')
        with DbSession() as session:
            fileSetModel = session.query(FileSetModel).filter_by(name=name).one()
            fileSet = FileSet(fileSetModel=fileSetModel)
        return fileSet
    
    def fileSets(self) -> List[FileSet]:
        with DbSession() as session:
            fileSetModels = session.query(FileSetModel).all()
            fileSets = []
            for fileSetModel in fileSetModels:
                fileSets.append(FileSet(fileSetModel=fileSetModel))
        return fileSets
    
    # CREATE/IMPORT
    
    def importFile(self, filePath: str) -> FileSet:
        LOGGER.info(f'DataManager.importFile() filePath={filePath}')
        with DbSession() as session:
            fileSetPath = os.path.split(filePath)[0]
            fileSetName = fileSetPath.split(os.path.sep)[-1]
            fileSetModel = FileSetModel(name=fileSetName, path=fileSetPath)
            session.add(fileSetModel)
            fileName = os.path.split(filePath)[1]
            fileModel = FileModel(name=fileName, path=filePath, fileSetModel=fileSetModel)
            session.add(fileModel)
            session.commit()
            fileSet = FileSet(fileSetModel=fileSetModel)  # Don't use fileSet() because it mixes sessions!
            self.signal().progress.emit(100)
            self.signal().finished.emit(fileSet)
        return fileSet
    
    def importFileSet(self, fileSetPath: str, fileType: FileType=AllFileType) -> FileSet:
        LOGGER.info(f'DataManager.importFileSet() fileSetPath={fileSetPath}, fileType={fileType}')
        filesToIgnore = self.settings().value('filesToIgnore')
        LOGGER.info(f'DataManager.importFileSet() filesToIgnore={filesToIgnore}')
        nrFiles = 0
        for fileName in os.listdir(fileSetPath):
            filePath = os.path.join(fileSetPath, fileName)
            LOGGER.debug(f'DataManager.importFileSet() fileName={fileName}, filePath={filePath}')
            if fileName not in filesToIgnore and fileType.check(filePath=filePath):
                nrFiles +=1
        LOGGER.info(f'DataManager.importFileSet() Found {nrFiles} files')
        if nrFiles == 0:
            self.signal().finished.emit(None)
            return None
        i = 0
        with DbSession() as session:
            fileSetName = fileSetPath.split(os.path.sep)[-1]
            fileSetModel = FileSetModel(name=fileSetName, path=fileSetPath)
            session.add(fileSetModel)
            for fileName in os.listdir(fileSetPath):
                filePath = os.path.join(fileSetPath, fileName)
                if fileName not in filesToIgnore and fileType.check(filePath=filePath):
                    fileModel = FileModel(name=fileName, path=filePath, fileSetModel=fileSetModel)
                    session.add(fileModel)
                    progress = int((i + 1) / nrFiles * 100)
                    self.signal().progress.emit(progress)
                    i += 1
            session.commit()
            fileSet = FileSet(fileSetModel=fileSetModel)
        self.signal().finished.emit(fileSet)
        return fileSet
    
    # UPDATE

    def updateFileSet(self, fileSet: FileSet) -> FileSet:
        LOGGER.info(f'DataManager.updateFileSet() fileSet={fileSet}')
        if not fileSet.id():
            raise RuntimeError('Cannot update file set that has no ID')
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            fileSetModel.name = fileSet.name()
            session.commit()
            fileSet = FileSet(fileSetModel=fileSetModel)
        return fileSet

    # DELETE

    def deleteFileSet(self, fileSet: FileSet) -> None:
        LOGGER.info(f'DataManager.deleteFileSet() fileSet={fileSet}')
        if not fileSet.id():
            raise RuntimeError('Cannot update file set that has no ID')
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            session.delete(fileSetModel)
            session.commit()
        cache = ObjectCache()
        for file in fileSet.files():
            if cache.has(file.id()):
                cache.remove(file.id())

    def deleteAllFileSets(self) -> None:
        with DbSession() as session:
            cache = ObjectCache()
            fileSetModels = session.query(FileSetModel).all()
            for fileSetModel in fileSetModels:
                for fileModel in fileSetModel.fileModels:
                    if cache.has(fileModel.id):
                        cache.remove(fileModel.id)
                session.delete(fileSetModel)
            session.commit()