from typing import Any


class TaskSetting:
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        self._name = name
        self._displayName = displayName
        self._optional = optional
        self._defaultValue = None
        self._value = None

    def name(self) -> str:
        return self._name
    
    def displayName(self) -> str:
        return self._displayName
    
    def optional(self) -> bool:
        return self._optional
    
    def setValue(self, value: Any) -> None:
        self._value = value
        
    def value(self) -> Any:
        return self._value
    
    def setDefaultValue(self, defaultValue: Any) -> None:
        self._defaultValue = defaultValue

    def defaultValue(self) -> Any:
        return self._defaultValue