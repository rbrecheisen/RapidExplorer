from PySide6.QtWidgets import QWidget, QGroupBox, QComboBox, QLabel, QVBoxLayout

from data.datamanager import DataManager


class TaskSettingFileSetWidget(QComboBox):
    def __init__(self, parent: QWidget=None) -> None:
        super(TaskSettingFileSetWidget, self).__init__(parent=parent)
        self._dataManager = DataManager()
        self.initUi()

    def initUi(self) -> None:
        self.addItem(None)
        for fileSet in self._dataManager.fileSets():
            self.addItem(fileSet.name())