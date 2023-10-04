from typing import Optional
from models.dataset import Dataset
from models.datasetmodel import DatasetModel


class DatasetToDatasetModelMapper:
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset

    def execute(self) -> Optional[DatasetModel]:
        pass
