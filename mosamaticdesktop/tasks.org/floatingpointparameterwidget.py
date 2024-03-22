from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QVBoxLayout, QDoubleSpinBox

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget


class FloatingPointParameterWidget(ParameterWidget):
    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(FloatingPointParameterWidget, self).__init__(parameter=parameter, parent=parent)
        if self.parameter().defaultValue() is not None:
            self.parameter().setValue(self.parameter().defaultValue())
        self._floatingPointSpinBox = None
        self.initUi()

    def initUi(self) -> None:
        self._floatingPointSpinBox = QDoubleSpinBox(self)
        self._floatingPointSpinBox.setValue(self.parameter().defaultValue())
        self._floatingPointSpinBox.valueChanged.connect(self.valueChanged)
        self.layout().addWidget(QLabel(self.parameter().labelText()))
        self.layout().addWidget(self._floatingPointSpinBox)

    def valueChanged(self, value: int) -> None:
        self.parameter().setValue(value)