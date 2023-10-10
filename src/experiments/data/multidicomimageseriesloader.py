import pydicom

from typing import Dict
from PySide6.QtCore import QRunnable
from models.dataset import Dataset, FileSet
from signals.loaderprogresssignal import LoaderProgressSignal


class MultiDicomImageSeriesLoader(QRunnable):
    def __init__(self, dataset: Dataset) -> None:
        super(MultiDicomImageSeriesLoader, self).__init__()
        self.dataset = dataset
        self.data = {}
        self.signal = LoaderProgressSignal()

    def getData(self) -> Dict[str, FileSet]:
        return self.data
    
    def run(self):
        self.data = {}
        i = 0
        for fileSet in self.dataset.fileSets:
            self.data[fileSet.name] = []
            for file in fileSet.files:
                p = pydicom.dcmread(file.path)
                p.decompress('pylibjpeg')                
                self.data[fileSet.name].append(p)
                progress = int((i + 1) / self.dataset.nrFiles() * 100)
                self.signal.progress.emit(progress)
                i += 1
            self.data[fileSet.name].sort(key=lambda p: int(p.InstanceNumber))
        self.signal.done.emit(True)
