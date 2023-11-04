from rapidx.app.singleton import singleton
from rapidx.app.data.file.file import File
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel


@singleton
class FileCache:
    def __init__(self) -> None:
        self._data = {}

    def data(self):
        return self._data

    def add(self, file: File) -> None:
        if file.id() not in self._data.keys():
            self._data[file.id()] = file

    def remove(self, id: str) -> None:
        if id in self._data.keys():
            del self._data[id]

    def removeFileSet(self, fileSetModel: FileSetModel) -> None:
        for fileModel in fileSetModel.fileModels:
            self.remove(fileModel.id)

    def removeMultiFileSet(self, multiFileSetModel: MultiFileSetModel) -> None:
        for fileSetModel in multiFileSetModel.fileSetModels:
            self.removeFileSet(fileSetModel)
        
    def get(self, id: str) -> File:
        if id in self._data.keys():
            return self._data[id]
        return None

    def clear(self) -> None:
        self._data = {}