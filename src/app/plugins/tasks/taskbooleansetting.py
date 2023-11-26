from plugins.tasks.tasksetting import TaskSetting


class TaskBooleanSetting(TaskSetting):
    def __init__(self, name: str, value: bool, default: bool) -> None:
        super(TaskBooleanSetting, self).__init__(name=name, value=value)
        self._default = default

    def default(self) -> bool:
        return self._default