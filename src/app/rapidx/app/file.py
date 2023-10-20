from abc import ABC, abstractmethod


class File(ABC):
    def __init__(self, path: str) -> None:
        self._id = None
        self._path = path

    def id(self) -> int:
        return self._id
    
    def setId(self, id) -> None:
        self._id = id

    def path(self) -> str:
        return self._path

    @abstractmethod
    def data(self):
        pass
