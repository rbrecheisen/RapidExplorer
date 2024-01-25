from PySide6.QtWidgets import QWidget, QComboBox

from mosamaticdesktop.data.datamanager import DataManager


class FileSetComboBox(QComboBox):
    def __init__(self, parent: QWidget=None) -> None:
        super(FileSetComboBox, self).__init__(parent)
        self._dataManager = DataManager()
        self.loadItems()

    def loadItems(self) -> None:
        self.addItem(None)
        fileSets = self._dataManager.fileSets()
        for fileSet in fileSets:
            self.addItem(fileSet.name())

    def showPopup(self) -> None:
        self.clear()
        self.loadItems()
        return super().showPopup()
