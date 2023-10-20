import os

from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem

from rapidx.app.dataset import Dataset
from rapidx.app.datasetitem import DatasetItem
from rapidx.app.datasetstoragemanager import DatasetStorageManager


class DatasetTreeWidget(QTreeView):
    def __init__(self, parent) -> None:
        super(DatasetTreeWidget, self).__init__(parent)
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Datasets'])
        self._model.itemChanged.connect(self._itemChanged)
        self.setModel(self._model)

    def addDataset(self, dataset: Dataset) -> None:
        datasetNode = DatasetItem(model=self._model, dataset=dataset)
        for fileSet in dataset.fileSets():
            fileSetNode = QStandardItem(fileSet.name())
            datasetNode.appendRow(fileSetNode)
            for file in fileSet.files():
                fileName = os.path.split(file.path())[1]
                fileNode = QStandardItem(fileName)
                fileSetNode.appendRow(fileNode)
        self._model.appendRow(datasetNode)

    def _itemChanged(self, item) -> None:
        dataset = item.dataset()
        oldName = dataset.name()        
        newName = item.text()
        dataset.setName(newName)
        manager = DatasetStorageManager()
        manager.save(dataset)
        print(f'Updated dataset name: {oldName} > {newName}')
