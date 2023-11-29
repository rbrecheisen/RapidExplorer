from tasks.tasksetting import TaskSetting


class TaskSettingText(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskSettingText, self).__init__(name=name, displayName=displayName, optional=optional)
        self._maximumLength = 1024

    def setMaximumLength(self, maximumLength: int) -> None:
        self._maximumLength = maximumLength

    def maximumLength(self) -> int:
        return self._maximumLength