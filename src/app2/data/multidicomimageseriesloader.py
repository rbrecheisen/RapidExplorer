import pydicom

from data.models.dataset import Dataset


class MultiDicomImageSeriesLoader:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset

    def load(self) -> pydicom.FileDataset:
        """ TODO: What do we return here? A dictionary object? Or a 2D array? It's
        not clear what keys we should use for the file sets because they have no
        name currently. By default, we could create a name based on the file's 
        parent directory.
        """
        file = self.dataset.firstFile()
        return pydicom.dcmread(file.path)