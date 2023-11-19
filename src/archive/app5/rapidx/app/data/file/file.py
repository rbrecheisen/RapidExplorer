from typing import Any
from abc import ABC, abstractmethod

from rapidx.app.data.file.filemodel import FileModel


class File(ABC):
    def __init__(self, fileModel: FileModel) -> None:
        self._fileModel = fileModel

    def fileModel(self) -> FileModel:
        return self._fileModel

    def id(self) -> str:
        return self.fileModel().id

    # @abstractmethod
    def data(self):
        pass
