from PySide6.QtGui import QStandardItem, QFont

from data.registeredfilesetmodel import RegisteredFileSetModel


class FileSetItem(QStandardItem):
    def __init__(self, registeredFileSetModel: RegisteredFileSetModel) -> None:
        super(FileSetItem, self).__init__(registeredFileSetModel.name)
        self._registeredFileSetModel = registeredFileSetModel
        self.id = self._registeredFileSetModel.id
        self._loaded = self._registeredFileSetModel.loaded
        if not self._loaded:
            font = QFont()
            font.setItalic(True)
            self.setFont(font)
        else:
            font = QFont()
            font.setItalic(False)
            self.setFont(font)

    def registeredFileSetModel(self) -> RegisteredFileSetModel:
        return self._registeredFileSetModel

    def loaded(self) -> bool:
        return self._loaded