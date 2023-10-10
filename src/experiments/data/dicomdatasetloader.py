import pydicom

from typing import Dict
from PySide6.QtCore import QRunnable
from models.dataset import Dataset, FileSet
from signals.loaderprogresssignal import LoaderProgressSignal


class DicomDatasetLoader(QRunnable):
    def __init__(self, dataset: Dataset) -> None:
        super(DicomDatasetLoader, self).__init__()
        self._dataset = dataset
        self._data = {}
        self._signal = LoaderProgressSignal()

    def getData(self) -> Dict[str, FileSet]:
        return self._data
    
    def run(self):
        self._data = {}
        i = 0
        for fileSet in self._dataset.fileSets:
            self._data[fileSet.name] = []
            for file in fileSet.files:
                p = pydicom.dcmread(file.path)
                p.decompress('pylibjpeg')                
                self._data[fileSet.name].append(p)
                progress = int((i + 1) / self._dataset.nrFiles() * 100)
                self._signal.progress.emit(progress)
                i += 1
            self._data[fileSet.name].sort(key=lambda p: int(p.InstanceNumber))
        self._signal.done.emit(True)
