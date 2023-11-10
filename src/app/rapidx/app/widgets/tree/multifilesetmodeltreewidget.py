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
from rapidx.app.widgets.tree.fileitem import FileItem
from rapidx.app.widgets.tree.filesetitem import FileSetItem
from rapidx.app.widgets.tree.multifilesetitem import MultiFileSetItem
from rapidx.app.widgets.tree.fileitemmenu import FileItemMenu
from rapidx.app.widgets.tree.filesetitemmenu import FileSetItemMenu
from rapidx.app.widgets.tree.multifilesetitemmenu import MultiFileSetItemMenu


class MultiFileSetModelTreeWidget(QTreeView):
    def __init__(self, db: Db) -> None:
        super(MultiFileSetModelTreeWidget, self).__init__()
        self._db = db
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Data'])
        self._model.itemChanged.connect(self._itemChanged)
        self.setModel(self._model)
        self.loadModelsDataFromDatabase()

    def addData(self, multiFileSetModel: MultiFileSetModel, loaded: bool=True) -> None:
        multiFileSetModelItem = MultiFileSetItem(multiFileSetModel, loaded)
        multiFileSetModelItem.setEditable(False)
        fileSetModels = DbFilterByCommand(self._db, FileSetModel, multiFileSetModelId=multiFileSetModel.id).execute()
        for fileSetModel in fileSetModels:
            fileSetItem = FileSetItem(fileSetModel)
            fileSetItem.setEditable(False)
            multiFileSetModelItem.appendRow(fileSetItem)
            fileModels = DbFilterByCommand(self._db, FileModel, fileSetModelId=fileSetModel.id).execute()
            for fileModel in fileModels:
                fileItem = FileItem(fileModel)
                fileItem.setEditable(False)
                fileSetItem.appendRow(fileItem)
        self._model.appendRow(multiFileSetModelItem)

    def loadModelsDataFromDatabase(self):
        multiFileSetModels = DbQueryAllCommand(self._db, MultiFileSetModel).execute()
        for multiFileSetModel in multiFileSetModels:
            self.addData(multiFileSetModel, loaded=False)

    def _itemChanged(self, item) -> None:
        if isinstance(item, FileSetItem):
            DbUpdateCommand(self._db, FileSetModel, item.fileSetModel(), name=item.text()).execute()
        elif isinstance(item, MultiFileSetItem):
            DbUpdateCommand(self._db, MultiFileSetModel, item.multiFileSetModel(), name=item.text()).execute()
        else:
            pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        index = self.indexAt(event.pos())
        if index.isValid():
            globalPos = self.viewport().mapToGlobal(event.pos())
            if event.button() == Qt.RightButton:
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
            menu = MultiFileSetItemMenu(self, item, globalPos, db=self._db)

            menu.show()
        else:
            pass
