from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout

from mosamaticdesktop.tasks.parameter import Parameter

class ParameterWidget(QWidget):
    @classmethod
    def NAME(cls):
        return cls.__qualname__

    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(ParameterWidget, self).__init__(parent=parent)
        self._parameter = parameter
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(5, 5, 5, 5)
        self._layout.setSpacing(5)
        self.setLayout(self._layout)

    def parameter(self) -> Parameter:
        return self._parameter

    def name(self) -> str:
        return self._parameter.name()

    def labelText(self) -> str:
        labelText = self._parameter.labelText()
        if not self.optional():
            labelText += '*'
        return labelText
    
    def optional(self) -> bool:
        return self._parameter.optional()
    
    def visible(self) -> bool:
        return self._parameter.visible()
    
    def defaultValue(self) -> Any:
        return self._parameter.defaultValue()
    
    def value(self) -> Any:
        return self._parameter.value()
    
    def setValue(self, value: Any) -> None:
        self._parameter.setValue(value)

    def layout(self) -> QVBoxLayout:
        return self._layout
    
    def copy(self):
        raise NotImplementedError()