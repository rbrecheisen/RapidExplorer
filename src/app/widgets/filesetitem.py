from PySide6.QtGui import QStandardItem

from data.fileset import FileSet


class FileSetItem(QStandardItem):
    def __init__(self, fileSet: FileSet) -> None:
        print(f'FileSetItem.__init__() fileSet = {fileSet}')
        super(FileSetItem, self).__init__(fileSet.name())
        self._fileSet = fileSet

    def fileSet(self) -> FileSet:
        return self._fileSet