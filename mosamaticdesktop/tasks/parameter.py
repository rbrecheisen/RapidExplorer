from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout

class Parameter(QWidget):
    @classmethod
    def NAME(cls):
        return cls.__qualname__

    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(Parameter, self).__init__(parent=parent)
        self._name = name
        self._labelText = labelText
        if not optional and not self._labelText.endswith('*'):
            self._labelText = labelText + '*'
        self._optional = optional
        self._visible = visible
        self._defaultValue = defaultValue
        self._value = None
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(5, 5, 5, 5)
        self._layout.setSpacing(5)
        self.setLayout(self._layout)

    def name(self) -> str:
        return self._name

    def labelText(self) -> str:
        return self._labelText
    
    def optional(self) -> bool:
        return self._optional
    
    def visible(self) -> bool:
        return self._visible
    
    def defaultValue(self) -> Any:
        return self._defaultValue
    
    def value(self) -> Any:
        return self._value
    
    def setValue(self, value: Any) -> None:
        self._value = value

    def layout(self) -> QVBoxLayout:
        return self._layout
    
    def copy(self):
        raise NotImplementedError()