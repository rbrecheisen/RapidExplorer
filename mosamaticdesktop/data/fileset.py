from typing import List

from mosamaticdesktop.data.models.filesetmodel import FileSetModel
from mosamaticdesktop.data.file import File


class FileSet:
    def __init__(self, model: FileSetModel) -> None:
        self._id = model.id
        self._name = model.name
        self._path = model.path
        
        self._files = []
        for fileModel in model.fileModels:
            file = File(model=fileModel)
            self._files.append(file)

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name
    
    def setName(self, name: str) -> None:
        self._name = name
    
    def path(self) -> str:
        return self._path
    
    def addFile(self, file: File) -> None:
        self._files.append(file)

    def files(self) -> List[File]:
        return self._files

    def nrFiles(self) -> int:
        return len(self._files)