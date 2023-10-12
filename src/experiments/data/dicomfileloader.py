import pydicom

from typing import Dict
from PySide6.QtCore import QRunnable
# from loaders.loader import Loader
from models.dataset import Dataset
from models.fileset import FileSet
from models.dicomfile import DicomFile
from experiments.data.loaderprogresssignal import LoaderProgressSignal


class DicomFileLoader(QRunnable):
    def __init__(self, path: str) -> None:
        super(DicomFileLoader, self).__init__()
        self._path = path
        self._data = Dataset(path=path)
        self._signal = LoaderProgressSignal()

    def path(self) -> str:
        return self._path

    def data(self) -> Dataset:
        return self._data
    
    def signal(self) -> LoaderProgressSignal:
        return self._signal

    def run(self):
        # Load DICOM file
        p = pydicom.dcmread(self.path())
        p.decompress('pylibjpeg')
        # Build dataset
        file = DicomFile(path=self.path(), data=p)
        fileSet = FileSet(path=self.path())
        fileSet.addFile(file)
        self.data().addFileSet(fileSet)
        # Emit signals
        self.signal().progress.emit(100)
        self.signal().done.emit(True)
