from tasks.tasksettingtext import TaskSettingText


class TaskSettingFilePath(TaskSettingText):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible: bool=True) -> None:
        super(TaskSettingFilePath, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)