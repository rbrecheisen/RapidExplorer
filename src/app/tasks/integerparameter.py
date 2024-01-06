from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QVBoxLayout, QSpinBox

from tasks.parameter import Parameter


class IntegerParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(IntegerParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self._integerSpinBox = None
        self.initUi()

    def initUi(self) -> None:
        self._integerSpinBox = QSpinBox(self)
        self._integerSpinBox.setValue(self.defaultValue())
        self._integerSpinBox.valueChanged.connect(self.valueChanged)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.labelText()))
        layout.addWidget(self._integerSpinBox)
        self.setLayout(layout)

    def valueChanged(self, value: int) -> None:
        self.setValue(value)