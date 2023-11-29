import os

from typing import List

from data.file import File
from data.filesetmodel import FileSetModel


class FileSet:
    def __init__(self, fileSetModel: FileSetModel) -> None:
        self._fileSetModel = fileSetModel
        self._id = self._fileSetModel.id
        self._name = self._fileSetModel.name
        self._path = self._fileSetModel.path
        self._files = []
        for fileModel in self._fileSetModel.fileModels:
            file = File(fileModel=fileModel)
            self._files.append(file)
    
    def fileSetModel(self) -> FileSetModel:
        return self._fileSetModel

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name
    
    def setName(self, name: str) -> None:
        # File set name is the only thing you can change
        self._name = name
    
    def path(self) -> str:
        return self._path
    
    def files(self) -> List[File]:
        return self._files
    
    def nrFiles(self) -> int:
        return len(self.files())