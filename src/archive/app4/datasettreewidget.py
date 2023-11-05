import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel

from rapidx.app.dataset import Dataset
from rapidx.app.datasetitem import DatasetItem
from rapidx.app.filesetitem import FileSetItem
from rapidx.app.fileitem import FileItem
from rapidx.app.datasetstoragemanager import DatasetStorageManager


class DatasetTreeWidget(QTreeView):
    def __init__(self, parent) -> None:
        super(DatasetTreeWidget, self).__init__(parent)
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Datasets'])
        self._model.itemChanged.connect(self._itemChanged)
        self.setModel(self._model)
        self._loadDatasetsFromDatabase()

    def addDataset(self, dataset: Dataset) -> None:
        datasetNode = DatasetItem(model=self._model, dataset=dataset)
        for fileSet in dataset.fileSets():
            fileSetNode = FileSetItem(model=self._model, fileSet=fileSet)
            datasetNode.appendRow(fileSetNode)
            for file in fileSet.files():
                fileNode = FileItem(model=self._model, file=file)
                fileNode.setEditable(False)
                fileSetNode.appendRow(fileNode)
        self._model.appendRow(datasetNode)

    def _loadDatasetsFromDatabase(self) -> None:
        manager = DatasetStorageManager()
        datasets = manager.loadAll()
        for dataset in datasets:
            self.addDataset(dataset=dataset)

    def _itemChanged(self, item) -> None:
        dataObj = item.dataObj()
        dataObj.setName(item.text())
        manager = DatasetStorageManager()
        manager.save(dataObj)
        # print(f'Updated {dataObj} name: {oldName} > {newName}')
