import pydicom

from typing import Dict
from PySide6.QtCore import QRunnable
from models.dataset import Dataset, FileSet
from signals.loaderprogresssignal import LoaderProgressSignal


class DicomImageLoader(QRunnable):
    def __init__(self, dataset: Dataset) -> None:
        super(DicomImageLoader, self).__init__()
        self.dataset = dataset
        self.data = {}
        self.signal = LoaderProgressSignal()

    def getData(self) -> Dict[str, FileSet]:
        return self.data
    
    def getImage(self) -> pydicom.FileDataset:
        return self.data['fileSet'][0]

    def run(self):
        file = self.dataset.firstFile()
        p = pydicom.dcmread(file.path)
        p.decompress('pylibjpeg')
        self.data = {'fileSet': [p]}
        self.signal.progress.emit(100)
        self.signal.done.emit(True)