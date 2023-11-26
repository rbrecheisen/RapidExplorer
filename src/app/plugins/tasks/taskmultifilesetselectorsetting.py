from plugins.tasks.tasksetting import TaskSetting


class TaskMultiFileSetSelectorSetting(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskMultiFileSetSelectorSetting, self).__init__(name=name, displayName=displayName, optional=optional)