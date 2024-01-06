from PySide6.QtWidgets import QWidget, QComboBox

from settings.setting import Setting


class SettingOptionListWidget(QComboBox):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingOptionListWidget, self).__init__(parent=parent)
        self._setting = setting
        self.addItem(None)        
        self.currentIndexChanged.connect(self.settingChanged)

    def addOption(self, option: str) -> None:
        self.addItem(option)

    def settingChanged(self, index: int) -> None:
        value = self.currentText()
        if value:
            value = True if value == 'True' else False
            self._setting.setValue(value)