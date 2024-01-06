from PySide6.QtWidgets import QWidget, QComboBox

from data.datamanager import DataManager
from settings.setting import Setting


class SettingFileSetWidget(QComboBox):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingFileSetWidget, self).__init__(parent=parent)
        self._setting = setting
        self._dataManager = DataManager()
        self.addItem(None)
        for fileSet in self._dataManager.fileSets():
            self.addItem(fileSet.name())
        if self._setting.value():
            self.setCurrentText(self._setting.value())
        self.currentIndexChanged.connect(self.settingChanged)

    def settingChanged(self, index: int) -> None:
        value = self.currentText()
        if value:
            self._setting.setValue(value)