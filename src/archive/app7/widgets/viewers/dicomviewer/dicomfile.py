import pydicom
import pydicom.errors


class DicomFile:
    def __init__(self, filePath: str) -> None:
        self._filePath = filePath
        self._data = None
        try:
            self._data = pydicom.dcmread(self._filePath)
            self._data.decompress()
        except pydicom.errors.InvalidDicomError:
            print(f'File {self._filePath} is not a valid DICOM file')

    def filePath(self) -> str:
        return self._filePath

    def data(self) -> pydicom.FileDataset:
        return self._data