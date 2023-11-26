from plugins.tasks.tasksetting import TaskSetting


class TaskTextSetting(TaskSetting):
    def __init__(self, name: str, value: str) -> None:
        super(TaskTextSetting, self).__init__(name=name, value=value)