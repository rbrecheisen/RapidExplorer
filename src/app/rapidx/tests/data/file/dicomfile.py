import pydicom
import pydicom.errors

from rapidx.tests.data.file.file import File
from rapidx.tests.data.file.filemodel import FileModel
from rapidx.tests.data.file.dicomfileinvalidexception import DicomFileInvalidException


class DicomFile(File):
    def __init__(self, fileModel: FileModel) -> None:
        super(DicomFile, self).__init__(fileModel)
        try:
            self._data = pydicom.dcmread(self.fileModel().path())
        except pydicom.errors.InvalidDicomError as e:
            raise DicomFileInvalidException()
        self._data.decompress()

    def header(self, attributeName: str=None) -> pydicom.FileDataset:
        if attributeName:
            return self._data[attributeName]
        return self._data
    
    def data(self):
        return self._data
    
    def pixelData(self):
        return self.data().pixel_array
