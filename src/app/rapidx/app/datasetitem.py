from PySide6.QtGui import QStandardItemModel, QStandardItem

from rapidx.app.dataset import Dataset


class DatasetItem(QStandardItem):
    def __init__(self, model: QStandardItemModel, dataset: Dataset) -> None:
        super(DatasetItem, self).__init__(dataset.name())
        self._model = model
        self._dataset = dataset

    def dataset(self) -> Dataset:
        return self._dataset

    # def setName(self, name: str) -> None:
    #     manager = DatasetStorageManager()
    #     manager.updateDatasetName(oldName=self._dataset.name(), newName=name)
    #     self._dataset.setName(name)
    #     self.setText(name)
    #     print(f'Dataset name: {self._dataset.name()}')