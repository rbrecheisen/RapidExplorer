import pydicom

from typing import Dict
from loaders.loader import Loader
from models.dataset import Dataset
from models.fileset import FileSet
from models.dicomfile import DicomFile


class DicomFileLoader(Loader):
    """ HOE GAAN WE DIRECTORIES DOORSPITTEN OP ZOEK NAAR FILES? """
    def __init__(self, path: str) -> None:
        super(DicomImageLoader2, self).__init__(path)
        self._data = Dataset(path=path)

    def data(self) -> Dataset:
        return self._data

    def run(self):
        self.data().addFileSet(FileSet(path=path))
        p = pydicom.dcmread(self.path())
        p.decompress('pylibjpeg')
        self.data().firstFileSet().addFile(DicomFile(self.path(), p))
        self.signal().progress.emit(100)
        self.signal().done.emit(True)
