import pydicom

from rapidx.tests.data.filemodel import FileModel


class DicomFile:
    def __init__(self, fileModel: FileModel) -> None:
        self._fileModel = fileModel
        self._data = pydicom.dcmread(self._fileModel.path())

    def header(self, attributeName: str=None) -> pydicom.FileDataset:
        if attributeName:
            return self._data[attributeName]
        return self._data
    
    def pixelData(self):
        return self._data.pixel_array
