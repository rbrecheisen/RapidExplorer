from abc import ABC, abstractmethod


class File(ABC):
    def __init__(self, path: str) -> None:
        self._id = None
        self._fileSetId = None
        self._path = path

    def id(self) -> int:
        return self._id
    
    def setId(self, id) -> None:
        self._id = id

    def fileSetId(self) -> int:
        return self._fileSetId

    def setFileSetId(self, fileSetId: int) -> None:
        self._fileSetId = fileSetId

    def path(self) -> str:
        return self._path

    @abstractmethod
    def data(self):
        pass
