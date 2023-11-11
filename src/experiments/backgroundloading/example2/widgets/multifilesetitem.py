from PySide6.QtGui import QStandardItem, QFont

from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class MultiFileSetItem(QStandardItem):
    def __init__(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel, loaded: bool) -> None:
        super(MultiFileSetItem, self).__init__(registeredMultiFileSetModel.name)
        self._registeredMultiFileSetModel = registeredMultiFileSetModel
        if not loaded:
            font = QFont()
            font.setItalic(True)
            self.setFont(font)
            self.setText(self.text() + ' [not loaded]')

    # def multiFileSetModel(self) -> MultiFileSetModel:
    #     return self._multiFileSetModel
    