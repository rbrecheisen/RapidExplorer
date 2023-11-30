from tasks.tasksetting import TaskSetting


class TaskSettingFileSet(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible=True) -> None:
        super(TaskSettingFileSet, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)