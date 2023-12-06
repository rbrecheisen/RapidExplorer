from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QFont

from settings.setting import Setting


class SettingLabelWidget(QLabel):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingLabelWidget, self).__init__(parent=parent)
        self._setting = setting
        font = QFont()
        font.setItalic(True)
        self.setFont(font)
        self.setWordWrap(True)
        self.setText(self._setting.value())