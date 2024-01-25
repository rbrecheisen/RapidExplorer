from typing import Any

from PySide6.QtWidgets import QWidget, QLabel, QSpinBox

from mosamaticdesktop.tasks.parameter import Parameter


class IntegerParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, minimum: int=0, maximum: int=100, step: int=1, parent: QWidget=None) -> None:
        super(IntegerParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self._minimum = minimum
        self._maximum = maximum
        self._step = step
        self._integerSpinBox = None
        self.initUi()

    def minimum(self) -> int:
        return self._minimum
    
    def maximum(self) -> int:
        return self._maximum
    
    def step(self) -> int:
        return self._step

    def initUi(self) -> None:
        self._integerSpinBox = QSpinBox(self)
        self._integerSpinBox.setRange(self._minimum, self._maximum)
        self._integerSpinBox.setSingleStep(self._step)
        self._integerSpinBox.setValue(self.defaultValue())
        self._integerSpinBox.valueChanged.connect(self.valueChanged)
        self.layout().addWidget(QLabel(self.labelText()))
        self.layout().addWidget(self._integerSpinBox)

    def valueChanged(self, value: int) -> None:
        self.setValue(value)

    def copy(self):
        return IntegerParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
            minimum=self.minimum(),
            maximum=self.maximum(),
            step=self.step(),
        )