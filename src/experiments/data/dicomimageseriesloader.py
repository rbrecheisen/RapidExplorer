import pydicom

from typing import List
from models.dataset import Dataset
from signals.fileloaderprogresssignal import FileLoaderProgressSignal


class DicomImageSeriesLoader:
    def __init__(self, dataset: Dataset, progressSignal: FileLoaderProgressSignal=None) -> None:
        self.dataset = dataset
        self.progressSignal = progressSignal

    def load(self) -> List[pydicom.FileDataset]:
        fileSet = self.dataset.firstFileSet()
        i = 0
        images = []
        for file in fileSet.files:
            p = pydicom.dcmread(file.path)
            p.decompress('pylibjpeg')
            images.append(p)
            if self.progressSignal:
                progress = int((i + 1) / fileSet.nrFiles() * 100)
                self.progressSignal.progress.emit(progress)
                i += 1
        images.sort(key=lambda p: int(p.InstanceNumber))
        return images
 