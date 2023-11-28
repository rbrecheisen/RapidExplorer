import pydicom
import numpy as np

from data.file import File
from data.registeredfilemodel import RegisteredFileModel


class PathFile(File):
    def __init__(self, registeredFileModel: RegisteredFileModel) -> None:
        super(PathFile, self).__init__(registeredFileModel)
        self._path = registeredFileModel.path

    def path(self) -> str:
        return self._path