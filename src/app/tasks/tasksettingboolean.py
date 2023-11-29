from tasks.tasksetting import TaskSetting


class TaskSettingBoolean(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskSettingBoolean, self).__init__(name=name, displayName=displayName, optional=optional)
