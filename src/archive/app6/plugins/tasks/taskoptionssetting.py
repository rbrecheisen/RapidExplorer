from typing import List

from plugins.tasks.tasksetting import TaskSetting


class TaskOptionsSetting(TaskSetting):
    def __init__(self, name: str, displayName: str, optional: bool=False) -> None:
        super(TaskOptionsSetting, self).__init__(name=name, displayName=displayName, optional=optional)