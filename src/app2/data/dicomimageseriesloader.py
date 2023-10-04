import pydicom

from typing import List
from data.models.dataset import Dataset


class DicomImageSeriesLoader:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset

    def load(self) -> List[pydicom.FileDataset]:
        fileSet = self.dataset.firstFileSet()
        images = []
        for file in fileSet.files:
            images.append(pydicom.dcmread(file.path))
        # TODO: sort by instance number!
        return images