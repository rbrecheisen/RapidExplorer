import pydicom

from typing import List, Dict
from PySide6.QtCore import QRunnable
from models.dataset import Dataset, FileSet
from signals.loaderprogresssignal import LoaderProgressSignal


class DicomImageSeriesLoader(QRunnable):
    def __init__(self, dataset: Dataset) -> None:
        super(DicomImageSeriesLoader, self).__init__()
        self.dataset = dataset
        self.data = {}
        self.signal = LoaderProgressSignal()

    def getData(self) -> Dict[str, FileSet]:
        return self.data
    
    def getImageSeries(self) -> List[pydicom.FileDataset]:
        return self.data[list(self.data.keys())[0]]

    def run(self):
        fileSet = self.dataset.firstFileSet()
        i = 0
        self.data = {fileSet.name: []}
        for file in fileSet.files:
            p = pydicom.dcmread(file.path)
            p.decompress('pylibjpeg')
            self.data[fileSet.name].append(p)
            progress = int((i + 1) / fileSet.nrFiles() * 100)
            self.signal.progress.emit(progress)
            i += 1
        self.data[fileSet.name].sort(key=lambda p: int(p.InstanceNumber))
        self.signal.done.emit(True)
 