from PySide6.QtWidgets import QWidget, QDoubleSpinBox

from settings.setting import Setting


class SettingFloatingPointWidget(QDoubleSpinBox):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingFloatingPointWidget, self).__init__(parent=parent)
        self._setting = setting
        if self._setting.value():
            self.setValue(self._setting.value())
        self.valueChanged.connect(self.settingChanged)

    def setRange(self, minimum: float, maximum: float) -> None:
        self.setRange(minimum, maximum)

    def settingChanged(self, value: float) -> None:
        if value:
            self._setting.setValue(value)