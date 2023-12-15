from PySide6.QtWidgets import QWidget, QSpinBox

from settings.setting import Setting


class SettingIntegerWidget(QSpinBox):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingIntegerWidget, self).__init__(parent=parent)
        self._setting = setting
        self.setRange(self._setting.minimum(), self._setting.maximum())
        if self._setting.value():
            self.setValue(self._setting.value())
        self.valueChanged.connect(self.settingChanged)

    def settingChanged(self, value: int) -> None:
        if value:
            self._setting.setValue(value)