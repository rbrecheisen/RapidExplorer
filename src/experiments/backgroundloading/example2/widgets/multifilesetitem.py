from PySide6.QtGui import QStandardItem, QFont

from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class MultiFileSetItem(QStandardItem):
    def __init__(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> None:
        super(MultiFileSetItem, self).__init__(registeredMultiFileSetModel.name)
        self._registeredMultiFileSetModel = registeredMultiFileSetModel
        self.id = self._registeredMultiFileSetModel.id
        self._loaded = self._registeredMultiFileSetModel.loaded
        if not self._loaded:
            font = QFont()
            font.setItalic(True)
            self.setFont(font)
        else:
            font = QFont()
            font.setItalic(False)
            self.setFont(font)

    def registeredMultiFileSetModel(self) -> RegisteredMultiFileSetModel:
        return self._registeredMultiFileSetModel

    def loaded(self) -> bool:
        return self._loaded