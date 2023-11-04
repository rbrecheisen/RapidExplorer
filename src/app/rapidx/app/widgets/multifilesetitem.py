from PySide6.QtGui import QStandardItem

from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel


class MultiFileSetItem(QStandardItem):
    def __init__(self, multiFileSetModel: MultiFileSetModel) -> None:
        super(MultiFileSetItem, self).__init__(multiFileSetModel.name)
        self._multiFileSetModel = multiFileSetModel

    def multiFileSetModel(self) -> MultiFileSetModel:
        return self._multiFileSetModel