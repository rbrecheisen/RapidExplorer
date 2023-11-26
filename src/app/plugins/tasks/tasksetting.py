from typing import Any


class TaskSetting:
    def __init__(self, name: str, displayName: str) -> None:
        self._name = name
        self._displayName = displayName
        self._value = None

    def name(self) -> str:
        return self._name
    
    def displayName(self) -> str:
        return self._displayName
    
    def value(self) -> Any:
        return self._value
    
    def setValue(self, value: Any) -> None:
        self._value = value