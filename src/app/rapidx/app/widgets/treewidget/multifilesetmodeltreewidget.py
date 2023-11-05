from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItemModel, QMouseEvent

from rapidx.app.data.db.db import Db
from rapidx.app.data.db.dbfilterbycommand import DbFilterByCommand
from rapidx.app.data.db.dbqueryallcommand import DbQueryAllCommand
from rapidx.app.data.db.dbupdatecommand import DbUpdateCommand
from rapidx.app.data.db.dbdeletecommand import DbDeleteCommand
from rapidx.app.data.db.dbgetcommand import DbGetCommand
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.widgets.treewidget.fileitem import FileItem
from rapidx.app.widgets.treewidget.filesetitem import FileSetItem
from rapidx.app.widgets.treewidget.multifilesetitem import MultiFileSetItem
from rapidx.app.widgets.treewidget.fileitemmenu import FileItemMenu
from rapidx.app.widgets.treewidget.filesetitemmenu import FileSetItemMenu
from rapidx.app.widgets.treewidget.multifilesetitemmenu import MultiFileSetItemMenu


class MultiFileSetModelTreeWidget(QTreeView):
    def __init__(self, parent) -> None:
        super(MultiFileSetModelTreeWidget, self).__init__(parent)
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Data'])
        self._model.itemChanged.connect(self._itemChanged)
        self.setModel(self._model)
        self.loadDataFromDatabase()

    def addData(self, multiFileSetModel: MultiFileSetModel) -> None:
        with Db() as db:
            multiFileSetModelItem = MultiFileSetItem(multiFileSetModel)
            multiFileSetModelItem.setEditable(False)
            fileSetModels = DbFilterByCommand(db, FileSetModel, multiFileSetModelId=multiFileSetModel.id).execute()
            for fileSetModel in fileSetModels:
                fileSetItem = FileSetItem(fileSetModel)
                fileSetItem.setEditable(False)
                multiFileSetModelItem.appendRow(fileSetItem)
                fileModels = DbFilterByCommand(db, FileModel, fileSetModelId=fileSetModel.id).execute()
                for fileModel in fileModels:
                    fileItem = FileItem(fileModel)
                    fileItem.setEditable(False)
                    fileSetItem.appendRow(fileItem)
        self._model.appendRow(multiFileSetModelItem)

    def loadDataFromDatabase(self):
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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                globalPos = self.viewport().mapToGlobal(event.pos())
                self._handleRightClickEvent(index, globalPos)
                return
        super(MultiFileSetModelTreeWidget, self).mousePressEvent(event)
            
    def _handleRightClickEvent(self, index, globalPos) -> None:
        item = self._model.itemFromIndex(index)
        if isinstance(item, FileItem):
            menu = FileItemMenu(self, item, globalPos)
            menu.show()
        elif isinstance(item, FileSetItem):
            menu = FileSetItemMenu(self, item, globalPos)
            menu.show()
        elif isinstance(item, MultiFileSetItem):
            menu = MultiFileSetItemMenu(self, item, globalPos)
            menu.show()
        else:
            pass

    def _rightClickDeleteAction(self, item):
        with Db() as db:
            multiFileSetModel = DbGetCommand(db, MultiFileSetModel, item.multiFileSetModel().id).execute()
            cache = FileCache()
            cache.removeMultiFileSet(multiFileSetModel)
            DbDeleteCommand(db, MultiFileSetModel, multiFileSetModel.id).execute()
        self._model.clear()
        self.loadDataFromDatabase()
