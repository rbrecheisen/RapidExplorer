from typing import List

from plugins.tasks.tasksetting import TaskSetting


class TaskOptionsSetting(TaskSetting):
    def __init__(self, name: str, value: List[str]) -> None:
        super(TaskOptionsSetting, self).__init__(name=name, value=value)