from singleton import singleton
from data.filecontent import FileContent


@singleton
class FileContentCache:
    def __init__(self) -> None:
        self._cache = {}

    def get(self, id: str) -> FileContent:
        if id in self._cache.keys():
            return self._cache[id]
        
    def add(self, fileContent: FileContent) -> None:
        self._cache[fileContent.id()] = fileContent

    def remove(self, id: str) -> None:
        if id in self._cache.keys():
            del self._cache[id]

    def clear(self) -> None:
        self._cache = {}