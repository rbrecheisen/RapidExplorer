from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QVBoxLayout, QDoubleSpinBox

from mosamaticdesktop.tasks.parameter import Parameter


class FloatingPointParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(FloatingPointParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self._floatingPointSpinBox = None
        self.initUi()

    def initUi(self) -> None:
        self._floatingPointSpinBox = QDoubleSpinBox(self)
        self._floatingPointSpinBox.setValue(self.defaultValue())
        self._floatingPointSpinBox.valueChanged.connect(self.valueChanged)
        self.layout().addWidget(QLabel(self.labelText()))
        self.layout().addWidget(self._floatingPointSpinBox)

    def valueChanged(self, value: int) -> None:
        self.setValue(value)
    
    def copy(self):
        return FloatingPointParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue()
        )