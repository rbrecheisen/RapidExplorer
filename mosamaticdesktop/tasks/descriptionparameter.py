from typing import Any

from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy
from PySide6.QtGui import QFont

from mosamaticdesktop.tasks.parameter import Parameter


class DescriptionParameter(Parameter):
    def __init__(self, name: str, description: str, parent: QWidget=None) -> None:
        super(DescriptionParameter, self).__init__(
            name=name, labelText=description, optional=True, parent=parent)
        self.initUi()

    def initUi(self) -> None:
        font = QFont()
        label = QLabel(self.labelText())
        label.setFont(font)
        label.setWordWrap(True)
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        label.setSizePolicy(policy)
        self.layout().addWidget(label)

    def copy(self):
        return DescriptionParameter(
            name=self.name(), 
            description=self.labelText()
        )