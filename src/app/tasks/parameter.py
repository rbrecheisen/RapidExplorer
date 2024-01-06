from typing import Any

from PySide6.QtWidgets import QWidget


class Parameter(QWidget):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(Parameter, self).__init__(parent=parent)
        self._name = name
        self._labelText = labelText
        self._optional = optional
        self._visible = visible
        self._defaultValue = defaultValue
        self._value = None

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