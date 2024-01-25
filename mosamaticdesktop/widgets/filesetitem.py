import os

from PySide6.QtGui import QStandardItem, QFont

from mosamaticdesktop.data.fileset import FileSet


class FileSetItem(QStandardItem):
    def __init__(self, fileSet: FileSet) -> None:
        super(FileSetItem, self).__init__(fileSet.name())
        self._fileSet = fileSet
        deleted = False
        for file in self._fileSet.files():
            if not os.path.isfile(file.path()):
                deleted = True
                break
        if deleted:
            font = QFont()
            font.setItalic(True)
            self.setFont(font)
            self.setText(self._fileSet.name() + '[some or all files deleted]')

    def fileSet(self) -> FileSet:
        return self._fileSet