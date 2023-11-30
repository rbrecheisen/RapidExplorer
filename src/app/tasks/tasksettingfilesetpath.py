from tasks.tasksettingtext import TaskSettingText


class TaskSettingFileSetPath(TaskSettingText):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible: bool=True) -> None:
        super(TaskSettingFileSetPath, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)