from PySide6.QtGui import QStandardItemModel, QStandardItem

from dataset import Dataset


class DatasetItem(QStandardItem):
    def __init__(self, model: QStandardItemModel, dataset: Dataset) -> None:
        super(DatasetItem, self).__init__(dataset.name())
        self._model = model
        self._dataset = dataset

    def setName(self, name: str) -> None:
        self._dataset.setName(name)
        self.setText(name)
        print(f'Dataset name: {name}')