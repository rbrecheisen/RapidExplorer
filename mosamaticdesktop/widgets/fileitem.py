import os

from PySide6.QtGui import QStandardItem, QFont

from mosamaticdesktop.data.file import File


class FileItem(QStandardItem):
    def __init__(self, file: File) -> None:
        super(FileItem, self).__init__(file.name())
        self._file = file
        if not os.path.isfile(self._file.path()):
            font = QFont()
            font.setItalic(True)
            self.setFont(font)
            self.setText(self._file.name() + '[deleted]')

    def file(self) -> File:
        return self._file