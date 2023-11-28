from singleton import singleton
from data.file import File
from data.registeredfilesetmodel import RegisteredFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


@singleton
class FileCache:
    def __init__(self) -> None:
        self._data = {}

    def data(self):
        return self._data

    def nrFiles(self) -> None:
        return len(self._data.keys())
    
    def printFiles(self) -> None:
        if self.nrFiles() == 0:
            print('{}')
        else:
            for k, v in self._data.items():
                print(f'{k}: {v}')

    def has(self, id: str) -> bool:
        return id in self._data.keys()

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

    def removeAllData(self) -> None:
        self._data.clear()
        self._data = {}
        
    def get(self, id: str) -> File:
        if id in self._data.keys():
            return self._data[id]
        return None

    def clear(self) -> None:
        print('Clearing cache...')
        self._data = {}