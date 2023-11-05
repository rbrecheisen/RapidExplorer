import os

from PySide6.QtGui import QStandardItem

from rapidx.app.data.file.filemodel import FileModel


class FileItem(QStandardItem):
    def __init__(self, fileModel: FileModel) -> None:
        super(FileItem, self).__init__(os.path.split(fileModel.path)[1])
        self._fileModel = fileModel

    def fileModel(self) -> FileModel:
        return self._fileModel