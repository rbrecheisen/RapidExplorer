from plugins.tasks.tasksetting import TaskSetting


class TaskFloatingPointSetting(TaskSetting):
    def __init__(self, name: str, value: float) -> None:
        super(TaskFloatingPointSetting, self).__init__(name=name, value=value)