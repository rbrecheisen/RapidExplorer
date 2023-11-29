from tasks.tasksetting import TaskSetting


class TaskSettingOptionList(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskSettingOptionList, self).__init__(name=name, displayName=displayName, optional=optional)