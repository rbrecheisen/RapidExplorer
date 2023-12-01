from PySide6.QtGui import QStandardItem

from data.fileset import FileSet


class FileSetItem(QStandardItem):
    def __init__(self, fileSet: FileSet) -> None:
        super(FileSetItem, self).__init__(fileSet.name())
        self._fileSet = fileSet

    def fileSet(self) -> FileSet:
        return self._fileSet