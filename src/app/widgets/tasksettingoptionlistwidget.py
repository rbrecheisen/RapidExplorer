from PySide6.QtWidgets import QWidget, QComboBox

from settings.setting import Setting


class TaskSettingOptionListWidget(QComboBox):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(TaskSettingOptionListWidget, self).__init__(parent=parent)
        self._setting = setting
        self.currentIndexChanged.connect(self.settingChanged)
        self.initUi()

    def initUi(self) -> None:
        self.addItem(None)

    def addOption(self, option: str) -> None:
        self.addItem(option)

    def settingChanged(self, index: int) -> None:
        value = self.currentText()
        if value:
            value = True if value == 'True' else False
            self._setting.setValue(value)