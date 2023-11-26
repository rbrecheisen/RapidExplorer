from plugins.tasks.tasksetting import TaskSetting


class TaskMultiFileSetSetting(TaskSetting):
    def __init__(self, name: str, displayName: str) -> None:
        super(TaskMultiFileSetSetting, self).__init__(name=name, displayName=displayName)