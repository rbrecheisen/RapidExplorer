from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView

from widgets.filesetitem import FileSetItem


class FileSetItemMenu(QMenu):
    def __init__(self, treeView: QTreeView, fileSetItem: FileSetItem, position: QPoint) -> None:
        super(FileSetItemMenu, self).__init__()
        self._treeView = treeView
        self._fileSetItem = fileSetItem
        self._position = position
        renameFileSetAction = self.addAction('Rename')
        renameFileSetAction.triggered.connect(self.renameFileSet)

    def renameFileSet(self):
        self._fileSetItem.setEditable(True)
        self._treeView.edit(self._treeView.model().indexFromItem(self._fileSetItem))
        self._fileSetItem.setEditable(False)

    def show(self):
        self.exec_(self._position)