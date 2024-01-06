from typing import List

from settings.setting import Setting
from settings.settingboolean import SettingBoolean
from settings.settingfilesetpath import SettingFileSetPath
from settings.settingfileset import SettingFileSet
from settings.settingfloatingpoint import SettingFloatingPoint
from settings.settinginteger import SettingInteger
from settings.settinglabel import SettingLabel
from settings.settingoptionlist import SettingOptionList
from settings.settingtext import SettingText


class Settings:
    def __init__(self, name: str) -> None:
        self._name = name
        self._settings = {}

    def name(self) -> str:
        return self._name

    def all(self) -> List[Setting]:
        return self._settings.values()
        
    def setting(self, name: str) -> Setting:
        return self._settings[name]
    
    def add(self, setting: Setting) -> None:
        self._settings[setting.name()] = setting

    def isTypeBoolean(self, setting: Setting) -> bool:
        return isinstance(setting, SettingBoolean)
    
    def isTypeFileSetPath(self, setting: Setting) -> bool:
        return isinstance(setting, SettingFileSetPath)

    def isTypeFileSet(self, setting: Setting) -> bool:
        return isinstance(setting, SettingFileSet)

    def isTypeFloatingPoint(self, setting: Setting) -> bool:
        return isinstance(setting, SettingFloatingPoint)

    def isTypeInteger(self, setting: Setting) -> bool:
        return isinstance(setting, SettingInteger)
    
    def isTypeLabel(self, setting: Setting) -> bool:
        return isinstance(setting, SettingLabel)

    def isTypeOptionList(self, setting: Setting) -> bool:
        return isinstance(setting, SettingOptionList)

    def isTypeText(self, setting: Setting) -> bool:
        return isinstance(setting, SettingText)