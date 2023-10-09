import pydicom

from typing import Dict
from models.dataset import Dataset
from signals.filesetloaderprogresssignal import FileSetLoaderProgressSignal


class MultiDicomImageSeriesLoader:
    def __init__(self, dataset: Dataset, progressSignal: FileSetLoaderProgressSignal=None) -> None:
        self.dataset = dataset
        self.progressSignal = progressSignal

    def load(self) -> Dict[str, pydicom.FileDataset]:
        images = {}
        for fileSet in self.dataset.fileSets:
            images[fileSet.name] = []
            for file in fileSet.files:
                p = pydicom.dcmread(file.path)
                p.decompress('pylibjpeg')                
                images[fileSet.name].append(p)
            images[fileSet.name].sort(key=lambda p: int(p.InstanceNumber))
            if self.progressSignal:
                # Emit signal
                print(f'Loaded file set {fileSet.name}')
                pass
        return images