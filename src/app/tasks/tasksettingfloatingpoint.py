from tasks.tasksetting import TaskSetting


class TaskSettingFloatingPoint(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskSettingFloatingPoint, self).__init__(name=name, displayName=displayName, optional=optional)
        self._minimum = 0.0
        self._maximum = 100.0

    def setMinimum(self, minimum: float) -> None:
        self._minimum = minimum

    def minimum(self) -> float:
        return self._minimum

    def setMaximum(self, maximum: float) -> None:
        self._maximum = maximum

    def maximum(self) -> float:
        return self._maximum