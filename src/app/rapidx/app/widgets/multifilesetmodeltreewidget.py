import os

from typing import List
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItemModel, QStandardItem

from rapidx.app.data.db import Db
# from rapidx.app.data.file import filemodel
# from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel


class MultiFileSetModelTreeWidget(QTreeView):
    def __init__(self, parent) -> None:
        super(MultiFileSetModelTreeWidget, self).__init__(parent)
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Data'])
        self._model.itemChanged.connect(self._itemChanged)
        self.setModel(self._model)
        self._loadDataFromDatabase()

    def addData(self, multiFileSetModel: MultiFileSetModel) -> None:
        with Db() as db:
            multiFileSetModelNode = QStandardItem(multiFileSetModel.name())
            fileSetModels = db.loadFileSetModels(multiFileSetModelId=multiFileSetModel.id())
            for fileSetModel in fileSetModels:
                fileSetNode = QStandardItem(fileSetModel.name())
                multiFileSetModelNode.appendRow(fileSetNode)
                fileModels = db.loadFileModels(fileSetModelId=fileSetModel.id())
                for fileModel in fileModels:
                    fileName = os.path.split(fileModel.path())[1]
                    fileNode = QStandardItem(fileName)
                    fileSetNode.appendRow(fileNode)
        self._model.appendRow(multiFileSetModelNode)

    def _loadDataFromDatabase(self):
        with Db() as db:
            multiFileSetModels = db.loadAll()
            for multiFileSetModel in multiFileSetModels:
                self.addData(multiFileSetModel)

    def _itemChanged(self, item) -> None:
        pass
