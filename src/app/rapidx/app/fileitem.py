import os

# from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from rapidx.app.file import File


class FileItem(QStandardItem):
    def __init__(self, model: QStandardItemModel, file: File) -> None:
        fileName = os.path.split(file.path())[1]
        super(FileItem, self).__init__(fileName)
        self._model = model
        self._file = file

    def dataObj(self) -> File:
        return self._file

    def __str__(self) -> str:
        return f'FileItem(file={self._file.path()})'