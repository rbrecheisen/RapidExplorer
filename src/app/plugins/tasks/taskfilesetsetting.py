from plugins.tasks.tasksetting import TaskSetting


class TaskFileSetSetting(TaskSetting):
    def __init__(self, name: str, displayName: str) -> None:
        super(TaskFileSetSetting, self).__init__(name=name, displayName=displayName)