from typing import Any

from PySide6.QtWidgets import QWidget, QLabel, QSpinBox

from mosamaticdesktop.tasks.integerparameter import IntegerParameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget


class IntegerParameterWidget(ParameterWidget):
    def __init__(self, parameter: IntegerParameter, parent: QWidget=None) -> None:
        super(IntegerParameterWidget, self).__init__(parameter=parameter, parent=parent)
        if self.parameter().defaultValue() is not None:
            self.parameter().setValue(self.parameter().defaultValue())
        self._integerSpinBox = None
        self.initUi()

    def initUi(self) -> None:
        self._integerSpinBox = QSpinBox(self)
        self._integerSpinBox.setRange(self.parameter().minimum(), self.parameter().maximum())
        self._integerSpinBox.setSingleStep(self.parameter().step())
        self._integerSpinBox.setValue(self.parameter().defaultValue())
        self._integerSpinBox.valueChanged.connect(self.valueChanged)
        self.layout().addWidget(QLabel(self.parameter().labelText()))
        self.layout().addWidget(self._integerSpinBox)

    def valueChanged(self, value: int) -> None:
        self.parameter().setValue(value)