from plugins.tasks.tasksetting import TaskSetting


class TaskBooleanSetting(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskBooleanSetting, self).__init__(name=name, displayName=displayName, optional=optional)
