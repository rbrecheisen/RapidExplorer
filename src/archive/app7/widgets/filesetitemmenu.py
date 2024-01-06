from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView, QMessageBox

from widgets.filesetitem import FileSetItem
from data.datamanager import DataManager


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
        self._treeView.clearFileSets()
        self._treeView.loadFileSetsFromDatabase()
        # resultCode = self.showFileSetDeleteWarning()
        # if resultCode == QMessageBox.Yes:
        #     shutil.rmtree(fileSet.path())

    def showFileSetDeleteWarning(self) -> int:
        messageBox = QMessageBox(self)
        messageBox.setWindowTitle('Warning')
        messageBox.setText('Do you want to delete the physical files as well?')
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return messageBox.exec_()

    def show(self):
        self.exec_(self._position)