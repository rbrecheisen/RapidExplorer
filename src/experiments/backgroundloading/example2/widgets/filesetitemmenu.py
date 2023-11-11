from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView

from widgets.filesetitem import FileSetItem


class FileSetItemMenu(QMenu):
    def __init__(self, treeView: QTreeView, fileSetItem: FileSetItem, position: QPoint, parent=None) -> None:
        super(FileSetItemMenu, self).__init__(parent)
        self._treeView = treeView
        self._item = fileSetItem
        self._position = position
        action1 = self.addAction('Rename')
        action2 = self.addAction('Show in Main View')
        action1.triggered.connect(self._handleRenameAction)
        action2.triggered.connect(self._handleShowInMainViewAction)

    def _handleRenameAction(self):
        pass

    def _handleShowInMainViewAction(self):
        pass

    def show(self):
        self.exec_(self._position)