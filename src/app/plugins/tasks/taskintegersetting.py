from plugins.tasks.tasksetting import TaskSetting


class TaskIntegerSetting(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskIntegerSetting, self).__init__(name=name, displayName=displayName, optional=optional)
        self._minimum = 0
        self._maximum = 100

    def setMinimum(self, minimum: int) -> None:
        self._minimum = minimum

    def minimum(self) -> int:
        return self._minimum

    def setMaximum(self, maximum: int) -> None:
        self._maximum = maximum

    def maximum(self) -> int:
        return self._maximum