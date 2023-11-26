from typing import Dict

from plugins.tasks.tasksetting import TaskSetting


class Task:
    def __init__(self, name: str) -> None:
        self._name = name
        # self._data = {}
        self._settings = {}

    def name(self) -> str:
        return self._name
    
    # def addData(self, data, name: str) -> None:
    #     # TODO: Remove this method because the task only specifies the "name" of the
    #     # dataset, not the dataset itself. The dataset itself is only retrieved when
    #     # the task is executed
    #     if name in self._data.keys():
    #         raise RuntimeError(f'Data with name {name} already added to task')
    #     self._data[name] = data

    # def hasData(self, name: str) -> bool:
    #     return name in self._data.keys()

    # def data(self, name: str):
    #     return self._data[name]
    
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
    
    def showSettingsDialog(self) -> None:
        raise NotImplementedError('Not implemented')

    def run(self) -> None:
        raise NotImplementedError('Not implemented')
    
    # def outputData(self):
    #     raise NotImplementedError('Not implemented')