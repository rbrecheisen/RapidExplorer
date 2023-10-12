import os

from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem

from dataset import Dataset


class DatasetTreeWidget(QTreeView):
    def __init__(self, parent) -> None:
        super(DatasetTreeWidget, self).__init__(parent)
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Datasets'])
        self.setModel(self._model)

    def addDataset(self, dataset: Dataset) -> None:
        datasetNode = QStandardItem(dataset.name())
        for fileSet in dataset.fileSets():
            fileSetNode = QStandardItem(fileSet.name())
            datasetNode.appendRow(fileSetNode)
            for file in fileSet.files():
                fileName = os.path.split(file.path())[1]
                fileNode = QStandardItem(fileName)
                fileSetNode.appendRow(fileNode)
        self._model.appendRow(datasetNode)
