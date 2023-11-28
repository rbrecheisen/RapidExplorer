from plugins.tasks.tasksetting import TaskSetting


class TaskFileSetSelectorSetting(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskFileSetSelectorSetting, self).__init__(name=name, displayName=displayName, optional=optional)