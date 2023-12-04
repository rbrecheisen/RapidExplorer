import os
import re

from typing import List

from PySide6.QtCore import QSettings

from data.datamanagersignal import DataManagerSigal
from data.dbsession import DbSession
from data.objectcache import ObjectCache
from data.filemodel import FileModel
from data.fileset import FileSet
from data.filesetmodel import FileSetModel

SETTINGSFILEPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


class DataManager:
    def __init__(self) -> None:
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self._signal = DataManagerSigal()

    def settings(self) -> QSettings:
        return self._settings
    
    def signal(self) -> DataManagerSigal:
        return self._signal
    
    # GET
    
    def fileSet(self, id: str) -> FileSet:
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, id)
            fileSet = FileSet(fileSetModel=fileSetModel)
        return fileSet
    
    def fileSetByName(self, name: str) -> FileSet:
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
        with DbSession() as session:
            fileSetModel = FileSetModel(path=os.path.split(filePath)[0])
            session.add(fileSetModel)
            fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
            session.add(fileModel)
            session.commit()
            fileSet = FileSet(fileSetModel=fileSetModel)  # Don't use fileSet() because it mixes sessions!
            self.signal().progress.emit(100)
            self.signal().finished.emit(fileSet)
        return fileSet
    
    def importFileSet(self, fileSetPath: str, regex: str=r'.*') -> FileSet:
        # Count files to be able to show progress
        filesToIgnore = self.settings().value('filesToIgnore')
        nrFiles = 0
        for f in os.listdir(fileSetPath):
            if f not in filesToIgnore and re.match(regex, f):
                nrFiles += 1
        i = 0
        with DbSession() as session:
            fileSetModel = FileSetModel(path=fileSetPath)
            session.add(fileSetModel)
            for fileName in os.listdir(fileSetPath):
                if fileName in filesToIgnore:
                    continue
                if re.match(regex, fileName):
                    filePath = os.path.join(fileSetPath, fileName)
                    fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
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