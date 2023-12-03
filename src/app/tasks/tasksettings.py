from typing import List

from tasks.tasksetting import TaskSetting
from tasks.tasksettingboolean import TaskSettingBoolean
from tasks.tasksettingfilesetpath import TaskSettingFileSetPath
from tasks.tasksettingfileset import TaskSettingFileSet
from tasks.tasksettingfloatingpoint import TaskSettingFloatingPoint
from tasks.tasksettinginteger import TaskSettingInteger
from tasks.tasksettingoptionlist import TaskSettingOptionList
from tasks.tasksettingtext import TaskSettingText


class TaskSettings:
    def __init__(self, taskName: str) -> None:
        self._taskName = taskName
        self._settings = {}

    def taskName(self) -> str:
        return self._taskName

    def all(self) -> List[TaskSetting]:
        return self._settings.values()
        
    def setting(self, name: str) -> TaskSetting:
        return self._settings[name]
    
    def add(self, setting: TaskSetting) -> None:
        self._settings[setting.name()] = setting

    def isTypeBoolean(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskSettingBoolean)
    
    def isTypeFileSetPath(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskSettingFileSetPath)

    def isTypeFileSet(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskSettingFileSet)

    def isTypeFloatingPoint(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskSettingFloatingPoint)

    def isTypeInteger(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskSettingInteger)

    def isTypeOptionList(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskSettingOptionList)

    def isTypeText(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskSettingText)