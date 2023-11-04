import os

from typing import List
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItemModel, QStandardItem

from rapidx.app.data.db.db import Db
from rapidx.app.data.db.dbfilterbycommand import DbFilterByCommand
from rapidx.app.data.db.dbqueryallcommand import DbQueryAllCommand
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
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
            multiFileSetModelNode = QStandardItem(multiFileSetModel.name)
            fileSetModels = DbFilterByCommand(db, FileSetModel, multiFileSetModelId=multiFileSetModel.id).execute()
            for fileSetModel in fileSetModels:
                fileSetNode = QStandardItem(fileSetModel.name)
                multiFileSetModelNode.appendRow(fileSetNode)
                fileModels = DbFilterByCommand(db, FileModel, fileSetModelId=fileSetModel.id).execute()
                for fileModel in fileModels:
                    fileName = os.path.split(fileModel.path)[1]
                    fileNode = QStandardItem(fileName)
                    fileNode.setEditable(False)
                    fileSetNode.appendRow(fileNode)
        self._model.appendRow(multiFileSetModelNode)

    def _loadDataFromDatabase(self):
        with Db() as db:
            # multiFileSetModels = db.loadAll()
            multiFileSetModels = DbQueryAllCommand(db, MultiFileSetModel).execute()
            for multiFileSetModel in multiFileSetModels:
                self.addData(multiFileSetModel)

    def _itemChanged(self, item) -> None:
        pass
