import pydicom

from abc import ABC, abstractmethod
from typing import Dict
from PySide6.QtCore import QRunnable
from models.dataset import Dataset, FileSet
from signals.loaderprogresssignal import LoaderProgressSignal


class ImageLoader(QRunnable, ABC):                  # Generic file set loader?
    def __init__(self, path: str) -> None:
        self._path = path
        self._signal = LoaderProgressSignal()

    def path(self) -> str:
        return self._path
    
    def signal(self) -> LoaderProgressSignal:
        return self._signal
    
    @abstractmethod
    def run(self):
        pass


class DicomImageLoader2(ImageLoader):
    def __init__(self, path: str) -> None:
        super(DicomImageLoader2, self).__init__(path)
        self._data = Dataset(path=path, name='Dataset')             # Create random name
        self._data.addFileSet(FileSet(path=path, name='FileSet'))   # Create random name

    def run(self):
        p = pydicom.dcmread(self.path())
        p.decompress('pylibjpeg')
        self._data.firstFileSet().addFile(DicomFile(...))



class DicomImageLoader(QRunnable):
    def __init__(self, dataset: Dataset) -> None:
        super(DicomImageLoader, self).__init__()
        self._dataset = dataset
        self._data = {}
        self._signal = LoaderProgressSignal()

    def getData(self) -> Dict[str, FileSet]:
        return self._data
    
    def getImage(self) -> pydicom.FileDataset:
        return self._data['fileSet'][0]

    def run(self):
        file = self._dataset.firstFile()
        p = pydicom.dcmread(file.path)
        p.decompress('pylibjpeg')
        self._data = {'fileSet': [p]}
        self._signal.progress.emit(100)
        self._signal.done.emit(True)