import os

from data.filemodel import FileModel


class File:
    def __init__(self, fileModel: FileModel) -> None:
        self._fileModel = fileModel
        self._id = self._fileModel.id
        self._name = os.path.split(self._fileModel.path)[1]
        self._path = self._fileModel.path

    def fileModel(self) -> FileModel:
        return self._fileModel
        
    def id(self) -> str:
        return self._id
    
    def name(self) -> str:
        return self._name
    
    def path(self) -> str:
        return self._path