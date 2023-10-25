import pydicom

from rapidx.app.file import File


class DicomFile(File):
    def __init__(self, path: str, data: pydicom.FileDataset) -> None:
        super(DicomFile, self).__init__(path)
        self._data = data

    def data(self) -> pydicom.FileDataset:
        return self._data

    def __str__(self) -> str:
        return f'DicomFile(path={self.path()})'