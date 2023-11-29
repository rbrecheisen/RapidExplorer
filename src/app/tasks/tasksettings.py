from typing import List

from tasks.tasksetting import TaskSetting


class TaskSettings:
    def __init__(self) -> None:
        self._settings = {}

    def setting(self, name: str) -> TaskSetting:
        return self._settings[name]
    
    def add(self, setting: TaskSetting) -> None:
        self._settings[setting.name()] = setting

    def settings(self) -> List[TaskSetting]:
        return self._settings.values()