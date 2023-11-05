from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

from rapidx.app.data.db.db import Db
from rapidx.app.data.db.dbdeletecommand import DbDeleteCommand
from rapidx.app.data.db.dbgetcommand import DbGetCommand
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.widgets.tree.multifilesetitem import MultiFileSetItem


class MultiFileSetItemMenu(QMenu):
    def __init__(self, treeView, item: MultiFileSetItem, position: QPoint, parent=None) -> None:
        super(MultiFileSetItemMenu, self).__init__(parent)
        self._treeView = treeView
        self._item = item
        self._position = position
        renameAction = self.addAction('Rename')
        showInMainViewAction = self.addAction('Show in Main View')
        deleteAction = self.addAction('Delete')
        renameAction.triggered.connect(self._handleRenameAction)
        showInMainViewAction.triggered.connect(self._handleShowInMainViewAction)
        deleteAction.triggered.connect(self._handleDeleteAction)

    def _handleRenameAction(self):
        self._item.setEditable(True)
        self._treeView.edit(self._treeView.model().indexFromItem(self._item))
        self._item.setEditable(False)

    def _handleShowInMainViewAction(self):
        pass

    def _handleDeleteAction(self):
        with Db() as db:
            multiFileSetModel = DbGetCommand(db, MultiFileSetModel, self._item.multiFileSetModel().id).execute()
            cache = FileCache()
            cache.removeMultiFileSet(multiFileSetModel)
            DbDeleteCommand(db, MultiFileSetModel, multiFileSetModel.id).execute()
        self._treeView.model().clear()
        self._treeView.loadDataFromDatabase()

    def show(self):
        self.exec_(self._position)