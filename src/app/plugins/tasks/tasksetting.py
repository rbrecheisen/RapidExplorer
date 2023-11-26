from typing import Any


class TaskSetting:
    def __init__(self, name: str, value: Any) -> None:
        self._name = name
        self._value = value

    def name(self) -> str:
        return self._name
    
    def value(self) -> Any:
        return self._value