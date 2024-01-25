from typing import Any

from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy
from PySide6.QtGui import QFont

from mosamaticdesktop.tasks.parameter import Parameter


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
        self.layout().addWidget(label)

    def copy(self):
        return LabelParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
        )