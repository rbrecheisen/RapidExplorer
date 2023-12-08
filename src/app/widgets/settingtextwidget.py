from PySide6.QtWidgets import QWidget, QLineEdit

from settings.setting import Setting


class SettingTextWidget(QLineEdit):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingTextWidget, self).__init__(parent=parent)
        self._setting = setting
        if self._setting.value():
            self.setText(self._setting.value())
        self.textChanged.connect(self.settingChanged)

    def settingChanged(self, text) -> None:
        self._setting.setValue(text)