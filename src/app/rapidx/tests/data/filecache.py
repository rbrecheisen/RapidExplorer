from rapidx.tests.singleton import singleton
from rapidx.tests.data.file import File


@singleton
class FileCache:
    def __init__(self) -> None:
        self._data = {}

    def add(self, file: File) -> None:
        if file.id() not in self._data.keys():
            self._data[file.id()] = file

    def remove(self, id: str) -> None:
        if id in self._data.keys():
            del self._data[id]
        
    def get(self, id: str) -> File:
        if id in self._data.keys():
            return self._data[id]
        return None

    def clear(self) -> None:
        self._data = {}