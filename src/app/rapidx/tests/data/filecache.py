from rapidx.tests.singleton import singleton
from rapidx.tests.data.file import File


@singleton
class FileCache:
    def __init__(self) -> None:
        self._data = {}

    def addFile(self, file) -> None:
        if file.id() not in self._data.keys():
            self._data[file.id()] = file
        else:
            raise RuntimeError(f'Key {file.id()} already exists')
        
    def file(self, id: str) -> File:
        return self._data[id]

    def clear(self, id: str=None) -> None:
        if id: 
            del self._data[id]
        else:
            self._data = {}