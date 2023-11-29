import os
import re

from typing import List

from PySide6.QtCore import QSettings

from data.progresssignal import ProgressSignal
from data.dbsession import DbSession
from data.objectcache import ObjectCache
from data.filemodel import FileModel
from data.fileset import FileSet
from data.filesetmodel import FileSetModel

SETTINGSFILEPATH = 'settings.ini'


class DataManager:
    def __init__(self) -> None:
        self._signal = ProgressSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)

    def signal(self) -> ProgressSignal:
        return self._signal
    
    def settings(self) -> QSettings:
        return self._settings
    
    # GET
    
    def getFileSet(self, id: str) -> FileSet:
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, id)
            fileSet = FileSet(fileSetModel=fileSetModel)
        return fileSet
    
    # CREATE
    
    def createFileSetFromFilePath(self, filePath: str) -> FileSet:
        with DbSession() as session:
            # Each file should have a parent file set
            fileSetModel = FileSetModel(path=os.path.split(filePath)[0])
            session.add(fileSetModel)
            fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
            session.add(fileModel)
            session.commit()
            fileSet = self.getFileSet(fileSetModel.id)
        return fileSet
    
    def createFileSetFromFileSetPath(self, fileSetPath: str, regex: str=r'.*') -> FileSet:
        with DbSession() as session:
            fileSetModel = FileSetModel(path=fileSetPath)
            session.add(fileSetModel)
            for fileName in os.listdir(fileSetPath):
                filesToIgnore = self.settings().value('filesToIgnore')
                if fileName in filesToIgnore:
                    continue
                if re.match(regex, fileName):
                    filePath = os.path.join(fileSetPath, fileName)
                    fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
                    session.add(fileModel)
            session.commit()
            fileSet = FileSet(fileSetModel=fileSetModel)
        return fileSet
    
    # UPDATE

    def updateFileSet(self, fileSet: FileSet) -> FileSet:
        if not fileSet.id():
            raise RuntimeError('Cannot update file set that has no ID')
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            fileSetModel.name = fileSet.name()
            session.commit()
            fileSet = self.getFileSet(fileSetModel.id)
        return fileSet

    # DELETE

    def deleteFileSet(self, fileSet: FileSet) -> None:
        if not fileSet.id():
            raise RuntimeError('Cannot update file set that has no ID')
        with DbSession() as session:
            fileSetModel = session.get(FileSetModel, fileSet.id())
            session.delete(fileSetModel)
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