from plugins.tasks.tasksetting import TaskSetting


class TaskIntegerSetting(TaskSetting):
    def __init__(self, name: str, value: int) -> None:
        super(TaskIntegerSetting, self).__init__(name=name, value=value)