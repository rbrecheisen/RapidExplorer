from singleton import singleton
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

    # TODO: Don't store registered file models here! We need real files with content
    # that have been loaded physically from the file system

    # def addFile(self, file: RegisteredFileModel) -> None:
    #     if file.id not in self._data.keys():
    #         self._data[file.id] = file

    # def addFileSet(self, fileSet: RegisteredFileSetModel) -> None:
    #     for file in fileSet.registeredFileModels:
    #         self.addFile(file)

    # def addMultiFileSet(self, multiFileSet: RegisteredMultiFileSetModel) -> None:
    #     for fileSet in multiFileSet.registeredFileSetModels:
    #         self.addFileSet(fileSet)

    # def removeFile(self, id: str) -> None:
    #     if id in self._data.keys():
    #         del self._data[id]

    # def removeFileSet(self, fileSet: RegisteredFileSetModel) -> None:
    #     for file in fileSet.registeredFileModels:
    #         self.removeFile(file.id)

    # def removeMultiFileSet(self, multiFileSet: RegisteredMultiFileSetModel) -> None:
    #     for fileSet in multiFileSet.registeredFileSetModels:
    #         self.removeFileSet(fileSet)
        
    # def get(self, id: str) -> RegisteredFileModel:
    #     if id in self._data.keys():
    #         return self._data[id]
    #     return None

    def clear(self) -> None:
        self._data = {}