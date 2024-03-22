from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QVBoxLayout

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget


class TextParameterWidget(ParameterWidget):
    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(TextParameterWidget, self).__init__(parameter=parameter, parent=parent)
        if self.parameter().defaultValue() is not None:
            self.parameter().setValue(self.parameter().defaultValue())
        self._pathLineEdit = None
        self.initUi()

    def initUi(self) -> None:
        self._pathLineEdit = QLineEdit(self)
        self._pathLineEdit.setText(self.parameter().defaultValue())
        self._pathLineEdit.textChanged.connect(self.pathChanged)
        self.layout().addWidget(QLabel(self.parameter().labelText()))
        self.layout().addWidget(self._pathLineEdit)

    def pathChanged(self, text) -> None:
        self.parameter().setValue(text)