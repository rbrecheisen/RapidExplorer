from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from rapidx.app.dataset import Dataset


class DatasetItem(QStandardItem):
    def __init__(self, model: QStandardItemModel, dataset: Dataset) -> None:
        super(DatasetItem, self).__init__(dataset.name())
        self._model = model
        self._dataset = dataset

    def dataObj(self) -> Dataset:
        return self._dataset
    
    def __str__(self) -> str:
        return f'DatasetItem(dataset={self._dataset.name()})'