from typing import Any

from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy
from PySide6.QtGui import QFont

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget


class LabelParameterWidget(ParameterWidget):
    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(LabelParameterWidget, self).__init__(parameter=parameter, parent=parent)
        self.initUi()

    def initUi(self) -> None:
        font = QFont()
        font.setItalic(True)
        label = QLabel('')
        label.setFont(font)
        label.setWordWrap(True)
        label.setText(self.parameter().labelText())
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        label.setSizePolicy(policy)
        self.layout().addWidget(label)