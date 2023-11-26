from plugins.tasks.tasksetting import TaskSetting


class TaskFileSetting(TaskSetting):
    def __init__(self, name: str, displayName: str) -> None:
        super(TaskFileSetting, self).__init__(name=name, displayName=displayName)
