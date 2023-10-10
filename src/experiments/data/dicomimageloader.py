import pydicom

from typing import Dict
from PySide6.QtCore import QRunnable
from models.dataset import Dataset, FileSet
from signals.loaderprogresssignal import LoaderProgressSignal


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