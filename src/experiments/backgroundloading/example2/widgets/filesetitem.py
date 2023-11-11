from PySide6.QtGui import QStandardItem

from data.registeredfilesetmodel import RegisteredFileSetModel


class FileSetItem(QStandardItem):
    def __init__(self, registeredFileSetModel: RegisteredFileSetModel) -> None:
        super(FileSetItem, self).__init__(registeredFileSetModel.name)
        self._registeredFileSetModel = registeredFileSetModel

    # def fileSetModel(self) -> FileSetModel:
    #     return self._fileSetModel