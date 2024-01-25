from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView, QMessageBox

from mosamaticdesktop.widgets.filesetitem import FileSetItem
from mosamaticdesktop.data.datamanager import DataManager


class FileSetItemMenu(QMenu):
    def __init__(self, treeView: QTreeView, fileSetItem: FileSetItem, position: QPoint) -> None:
        super(FileSetItemMenu, self).__init__()
        self._treeView = treeView
        self._fileSetItem = fileSetItem
        self._position = position
        self._dataManager = DataManager()
        renameFileSetAction = self.addAction('Rename')
        renameFileSetAction.triggered.connect(self.renameFileSet)
        deleteFileSetAction = self.addAction('Delete')
        deleteFileSetAction.triggered.connect(self.deleteFileSet)

    def renameFileSet(self):
        self._fileSetItem.setEditable(True)
        self._treeView.edit(self._treeView.model().indexFromItem(self._fileSetItem))
        self._fileSetItem.setEditable(False)

    def deleteFileSet(self):
        fileSet = self._fileSetItem.fileSet()
        self._dataManager.deleteFileSet(fileSet=fileSet)

    def show(self):
        self.exec_(self._position)