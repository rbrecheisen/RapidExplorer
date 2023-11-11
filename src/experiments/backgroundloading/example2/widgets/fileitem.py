import os

from PySide6.QtGui import QStandardItem

from data.registeredfilemodel import RegisteredFileModel


class FileItem(QStandardItem):
    def __init__(self, registeredFileModel: RegisteredFileModel) -> None:
        super(FileItem, self).__init__(os.path.split(registeredFileModel.path)[1])
        self._registeredFileModel = registeredFileModel

    # def fileModel(self) -> FileModel:
    #     return self._fileModel