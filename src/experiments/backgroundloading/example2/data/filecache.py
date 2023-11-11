from singleton import singleton
from data.file import File
from data.registeredfilemodel import RegisteredFileModel
from data.registeredfilesetmodel import RegisteredFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


@singleton
class FileCache:
    def __init__(self) -> None:
        self._data = {}

    def nrFiles(self) -> None:
        return len(self._data.keys())
    
    def printFiles(self) -> None:
        if self.nrFiles() == 0:
            print('{}')
        else:
            for k, v in self._data.items():
                print(f'{k}: {v}')

    def add(self, file: File) -> None:
        if file.id not in self._data.keys():
            self._data[file.id] = file

    def remove(self, id: str) -> None:
        if id in self._data.keys():
            del self._data[id]

    def removeFileSet(self, registeredFileSetModel: RegisteredFileSetModel) -> None:
        for registeredFileModel in registeredFileSetModel.registeredFileModels:
            self.remove(registeredFileModel.id)

    def removeMultiFileSet(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> None:
        for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
            self.removeFileSet(registeredFileSetModel)
        
    def get(self, id: str) -> File:
        if id in self._data.keys():
            return self._data[id]
        return None

    def clear(self) -> None:
        self._data = {}