from typing import List

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView, QMessageBox

from mosamaticdesktop.widgets.filesetitem import FileSetItem
from mosamaticdesktop.data.datamanager import DataManager


class MultiFileSetItemMenu(QMenu):
    def __init__(self, treeView: QTreeView, fileSetItems: List[FileSetItem], globalPos: QPoint) -> None:
        super(MultiFileSetItemMenu, self).__init__()
        self._treeView = treeView
        self._fileSetItems = fileSetItems
        self._position = globalPos
        self._dataManager = DataManager()
        deleteFileSetAction = self.addAction('Delete')
        deleteFileSetAction.triggered.connect(self.deleteFileSet)

    def deleteFileSet(self):
        for fileSetItem in self._fileSetItems:
            if isinstance(fileSetItem, FileSetItem):
                fileSet = fileSetItem.fileSet()
                self._dataManager.deleteFileSet(fileSet=fileSet)

    def show(self):
        self.exec_(self._position)