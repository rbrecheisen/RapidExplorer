import pydicom
import numpy as np

from data.file import File
from data.registeredfilemodel import RegisteredFileModel


class DicomFile(File):
    def __init__(self, registeredFileModel: RegisteredFileModel) -> None:
        super(DicomFile, self).__init__(registeredFileModel)
        self._data = pydicom.dcmread(registeredFileModel.path)
        self._data.decompress()

    def data(self) -> pydicom.FileDataset:
        return self._data

    def header(self, attributeName: str=None) -> str:
        if attributeName:
            return str(self._data[attributeName])
        return str(self.data())

    def pixelData(self) -> np.array:
        return self.data().pixel_array