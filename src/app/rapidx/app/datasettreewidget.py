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

    def _itemChanged(self, item) -> None:
        dataObj = item.dataObj()  # This can be Dataset, (Dicom)FileSet or (Dicom)File object
        oldName = dataObj.name()        
        newName = item.text()
        dataObj.setName(newName)
        manager = DatasetStorageManager()
        manager.save(dataObj)  # This method can only save whole datasets
        print(f'Updated {dataObj} name: {oldName} > {newName}')
