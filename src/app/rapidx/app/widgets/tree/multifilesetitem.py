from PySide6.QtGui import QStandardItem, QFont

from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel


class MultiFileSetItem(QStandardItem):
    def __init__(self, multiFileSetModel: MultiFileSetModel, loaded: bool=True) -> None:
        super(MultiFileSetItem, self).__init__(multiFileSetModel.name)
        self._multiFileSetModel = multiFileSetModel
        self._loaded = loaded
        if not self._loaded:
            font = QFont()
            font.setItalic(True)
            self.setFont(font)
            self.setText(self.text() + ' [not loaded]')

    def loaded(self) -> bool:
        return self._loaded

    def multiFileSetModel(self) -> MultiFileSetModel:
        return self._multiFileSetModel
    