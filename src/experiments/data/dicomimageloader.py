import pydicom

from models.dataset import Dataset


class DicomImageLoader:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset

    def load(self) -> pydicom.FileDataset:
        file = self.dataset.firstFile()
        p = pydicom.dcmread(file.path)
        p.decompress('pylibjpeg')
        return p