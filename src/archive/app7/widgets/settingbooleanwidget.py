from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QCheckBox

from settings.setting import Setting


class SettingBooleanWidget(QCheckBox):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingBooleanWidget, self).__init__(parent=parent)
        self._setting = setting
        if self._setting.value() is not None:
            self.setCheckState(Qt.Checked if self._setting.value() else Qt.Unchecked)
        elif self._setting.defaultValue():
            self.setCheckState(Qt.Checked)
        elif not self._setting.defaultValue():
            self.setCheckState(Qt.Unchecked)
        else:
            pass
        self.setText(self._setting.displayName())
        self.stateChanged.connect(self.settingChanged)

    def settingChanged(self, state: int) -> None:
        self._setting.setValue(True if state == Qt.Checked else False)