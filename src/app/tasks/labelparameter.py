from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QFont

from tasks.parameter import Parameter


class LabelParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(LabelParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        self.initUi()

    def initUi(self) -> None:
        font = QFont()
        font.setItalic(True)
        label = QLabel('')
        label.setFont(font)
        label.setWordWrap(True)
        label.setText(self.labelText())
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        label.setSizePolicy(policy)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
