from plugins.tasks.tasksetting import TaskSetting


class TaskFileSelectorSetting(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskFileSelectorSetting, self).__init__(name=name, displayName=displayName, optional=optional)