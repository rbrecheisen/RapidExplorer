from typing import Dict

from PySide6.QtWidgets import QDialog

from plugins.tasks.tasksetting import TaskSetting
from plugins.tasks.taskbooleansetting import TaskBooleanSetting
from plugins.tasks.taskintegersetting import TaskIntegerSetting
from plugins.tasks.taskfloatingpointsetting import TaskFloatingPointSetting
from plugins.tasks.tasktextsetting import TaskTextSetting
from plugins.tasks.taskoptionssetting import TaskOptionsSetting
from plugins.tasks.taskfilesetting import TaskFileSetting
from plugins.tasks.taskfilesetsetting import TaskFileSetSetting
from plugins.tasks.taskmultifilesetsetting import TaskMultiFileSetSetting
from plugins.tasks.tasksettingsdialog import TaskSettingsDialog


class Task:
    def __init__(self, name: str) -> None:
        self._name = name
        self._settings = {}

    def name(self) -> str:
        return self._name
    
    def addSetting(self, setting: TaskSetting) -> None:
        if setting.name() in self._settings.keys():
            raise RuntimeError(f'Setting with name {name} already added to task')
        self._settings[setting.name()] = setting

    def hasSetting(self, name) -> bool:
        return name in self._settings.keys()
    
    def setting(self, name: str) -> TaskSetting:
        return self._settings[name]
    
    def settings(self) -> Dict:
        return self._settings
    
    def checkSettingTypeIsBoolean(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskBooleanSetting)
    
    def checkSettingTypeIsInteger(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskIntegerSetting)
    
    def checkSettingTypeIsFloatingPoint(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskFloatingPointSetting)
    
    def checkSettingTypeIsText(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskTextSetting)
    
    def checkSettingTypeIsOptions(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskOptionsSetting)
    
    def checkSettingTypeIsFile(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskFileSetting)
    
    def checkSettingTypeIsFileSet(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskFileSetSetting)
    
    def checkSettingTypeIsMultiFileSet(self, setting: TaskSetting) -> bool:
        return isinstance(setting, TaskMultiFileSetSetting)
    
    def showSettingsDialog(self) -> None:
        settingsDialog = TaskSettingsDialog(task=self)
        resultCode = settingsDialog.show()
        if resultCode == QDialog.Accepted:
            print('Input data: {}'.format(self.setting('inputData').value()))
            print('TensorFlow model files: {}'.format(self.setting('tensorFlowModelFiles').value()))
        elif resultCode == QDialog.Rejected:
            print('Dialog rejected')
        else:
            raise RuntimeError(f'Unknown return code {resultCode}')

    def run(self) -> None:
        raise NotImplementedError('Not implemented')
    
    def outputData(self):
        raise NotImplementedError('Not implemented')