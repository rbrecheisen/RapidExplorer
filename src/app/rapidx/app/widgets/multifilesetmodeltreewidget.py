import os

from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItemModel

from rapidx.app.data.db.db import Db
from rapidx.app.data.db.dbfilterbycommand import DbFilterByCommand
from rapidx.app.data.db.dbqueryallcommand import DbQueryAllCommand
from rapidx.app.data.db.dbupdatecommand import DbUpdateCommand
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.widgets.fileitem import FileItem
from rapidx.app.widgets.filesetitem import FileSetItem
from rapidx.app.widgets.multifilesetitem import MultiFileSetItem


class MultiFileSetModelTreeWidget(QTreeView):
    def __init__(self, parent) -> None:
        super(MultiFileSetModelTreeWidget, self).__init__(parent)
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Data'])
        self._model.itemChanged.connect(self._itemChanged)
        self.setModel(self._model)
        self._loadDataFromDatabase()

    def addData(self, multiFileSetModel: MultiFileSetModel, db=None) -> None:
        with Db() as db:
            multiFileSetModelItem = MultiFileSetItem(multiFileSetModel)
            fileSetModels = DbFilterByCommand(db, FileSetModel, multiFileSetModelId=multiFileSetModel.id).execute()
            for fileSetModel in fileSetModels:
                fileSetItem = FileSetItem(fileSetModel)
                multiFileSetModelItem.appendRow(fileSetItem)
                fileModels = DbFilterByCommand(db, FileModel, fileSetModelId=fileSetModel.id).execute()
                for fileModel in fileModels:
                    fileItem = FileItem(fileModel)
                    fileItem.setEditable(False)
                    fileSetItem.appendRow(fileItem)
        self._model.appendRow(multiFileSetModelItem)

    def _loadDataFromDatabase(self):
        with Db() as db:
            multiFileSetModels = DbQueryAllCommand(db, MultiFileSetModel).execute()
        for multiFileSetModel in multiFileSetModels:
            self.addData(multiFileSetModel)

    def _itemChanged(self, item) -> None:
        with Db() as db:
            if isinstance(item, FileSetItem):
                DbUpdateCommand(db, FileSetModel, item.fileSetModel(), name=item.text()).execute()
            elif isinstance(item, MultiFileSetItem):
                DbUpdateCommand(db, MultiFileSetModel, item.multiFileSetModel(), name=item.text()).execute()
            else:
                pass
