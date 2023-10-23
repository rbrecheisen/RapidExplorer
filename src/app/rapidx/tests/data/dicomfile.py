import pydicom

from rapidx.tests.data.file import File
from rapidx.tests.data.filemodel import FileModel


class DicomFile(File):
    def __init__(self, fileModel: FileModel) -> None:
        super(DicomFile, self).__init__(fileModel)
        self._data = pydicom.dcmread(self.fileModel().path())

    def header(self, attributeName: str=None) -> pydicom.FileDataset:
        if attributeName:
            return self._data[attributeName]
        return self._data
    
    def data(self):
        return self._data.pixel_array
