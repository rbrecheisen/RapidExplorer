from abc import ABC, abstractmethod


class File(ABC):
    def __init__(self, path: str) -> None:
        self._path = path

    def path(self) -> str:
        return self._path

    @abstractmethod
    def data(self):
        pass
