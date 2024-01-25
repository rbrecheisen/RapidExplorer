from mosamaticdesktop.singleton import singleton
from mosamaticdesktop.data.filecontent import FileContent


@singleton
class FileContentCache:
    def __init__(self) -> None:
        self._cache = {}

    def get(self, id: str) -> FileContent:
        if self.has(id):
            return self._cache[id]
        return None
    
    def has(self, id: str) -> bool:
        return id in self._cache.keys()
        
    def add(self, fileContent: FileContent) -> None:
        self._cache[fileContent.id()] = fileContent

    def remove(self, id: str) -> None:
        if id in self._cache.keys():
            del self._cache[id]

    def clear(self) -> None:
        self._cache = {}