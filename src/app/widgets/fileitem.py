import os

from PySide6.QtGui import QStandardItem

from data.file import File


class FileItem(QStandardItem):
    def __init__(self, file: File) -> None:
        super(FileItem, self).__init__(os.path.split(file.path())[1])
        self._file = file

    def file(self) -> File:
        return self._file