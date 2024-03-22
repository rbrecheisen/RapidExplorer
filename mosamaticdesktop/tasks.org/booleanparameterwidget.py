from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QVBoxLayout, QCheckBox

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget


class BooleanParameterWidget(ParameterWidget):
    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(BooleanParameterWidget, self).__init__(parameter=parameter, parent=parent)
        self._booleanCheckBox = None
        self.initUi()

    def initUi(self) -> None:
        self._booleanCheckBox = QCheckBox(self)
        self._booleanCheckBox.setText(self.parameter().labelText())
        if self.parameter().defaultValue() is not None:
            self._booleanCheckBox.setCheckState(Qt.Checked if self.parameter().defaultValue() else Qt.Unchecked)
            self.stateChanged(state=self._booleanCheckBox.checkState())
        self._booleanCheckBox.stateChanged.connect(self.stateChanged)
        self.layout().addWidget(self._booleanCheckBox)

    def stateChanged(self, state: int) -> None:
        self.parameter().setValue(True if state == Qt.Checked else False)