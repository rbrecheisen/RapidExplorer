from tasks.tasksetting import TaskSetting


class TaskSettingBoolean(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible: bool=True, defaultValue: bool=True) -> None:
        super(TaskSettingBoolean, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)
        self._defaultValue = defaultValue
        self.setValue(self._defaultValue)

    def defaultValue(self) -> bool:
        return self._defaultValue