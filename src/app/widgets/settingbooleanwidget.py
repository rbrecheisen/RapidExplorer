from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QCheckBox

from settings.setting import Setting


class SettingBooleanWidget(QCheckBox):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingBooleanWidget, self).__init__(parent=parent)
        self._setting = setting
        self.stateChanged.connect(self.settingChanged)
        if self._setting.value():
            self.setCheckState(Qt.Checked if self._setting.value() else Qt.NotChecked)
        elif self._setting.defaultValue():
            self.setCheckState(Qt.Checked if self._setting.defaultValue() else Qt.NotChecked)

    def settingChanged(self, state: int) -> None:
        self._setting.setValue(True if state == Qt.Checked else False)