import os

from PySide6.QtGui import QStandardItem, QFont

from data.registeredfilemodel import RegisteredFileModel


class FileItem(QStandardItem):
    def __init__(self, registeredFileModel: RegisteredFileModel) -> None:
        super(FileItem, self).__init__(os.path.split(registeredFileModel.path)[1])
        self._registeredFileModel = registeredFileModel
        self.id = self._registeredFileModel.id
        self._loaded = self._registeredFileModel.loaded
        if not self._loaded:
            font = QFont()
            font.setItalic(True)
            self.setFont(font)
        else:
            font = QFont()
            font.setItalic(False)
            self.setFont(font)

    def registeredFileModel(self) -> RegisteredFileModel:
        return self._registeredFileModel

    def loaded(self) -> bool:
        return self._loaded