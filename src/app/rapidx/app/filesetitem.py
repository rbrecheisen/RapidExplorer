from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from rapidx.app.fileset import FileSet


class FileSetItem(QStandardItem):
    def __init__(self, model: QStandardItemModel, fileSet: FileSet) -> None:
        super(FileSetItem, self).__init__(fileSet.name())
        self._model = model
        self._fileSet = fileSet

    def dataObj(self) -> FileSet:
        return self._fileSet

    def __str__(self) -> str:
        return f'FileSetItem(fileSet={self._fileSet.name()})'