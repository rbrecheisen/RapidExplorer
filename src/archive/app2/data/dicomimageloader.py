import pydicom

from data.models.dataset import Dataset


class DicomImageLoader:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset

    def load(self) -> pydicom.FileDataset:
        file = self.dataset.firstFile()
        return pydicom.dcmread(file.path)