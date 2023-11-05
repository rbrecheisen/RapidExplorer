from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

from rapidx.app.widgets.treewidget.filesetitem import FileSetItem


class FileSetItemMenu(QMenu):
    def __init__(self, treeView, item: FileSetItem, position: QPoint, parent=None) -> None:
        super(FileSetItemMenu, self).__init__(parent)
        self._treeView = treeView
        self._item = item
        self._position = position
        renameAction = self.addAction('Rename')
        showInMainViewAction = self.addAction('Show in Main View')
        renameAction.triggered.connect(self._handleRenameAction)
        showInMainViewAction.triggered.connect(self._handleShowInMainViewAction)

    def _handleRenameAction(self):
        # self._item.setEditable(True)
        self._treeView.edit(self._treeView.model().indexFromItem(self._item))

    def _handleShowInMainViewAction(self):
        pass

    def show(self):
        self.exec_(self._position)