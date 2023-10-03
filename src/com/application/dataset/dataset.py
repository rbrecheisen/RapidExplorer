from abc import ABC, abstractmethod


class Dataset(ABC):

    def __init__(self) -> None:
        self._data = {}

    @abstractmethod
    def load(self, path: str) -> None:
        pass

    def data(self) -> {}:
        return self._data
