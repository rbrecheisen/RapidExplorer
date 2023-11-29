from typing import Dict

from PySide6.QtCore import QRunnable

from tasks.tasksignal import TaskSignal
from tasks.tasksettings import TaskSettings
from data.datamanager import DataManager


class Task(QRunnable):
    def __init__(self, name: str) -> None:
        super(Task, self).__init__()
        self._name = name
        self._settings = TaskSettings()
        self._signal = TaskSignal()
        self._dataManager = DataManager()
        self._nrSteps = 0

    def name(self) -> str:
        return self._name
    
    def settings(self) -> TaskSettings:
        return self._settings

    def signal(self) -> TaskSignal:
        return self._signal
    
    def dataManager(self) -> DataManager:
        return self._dataManager

    def nrSteps(self) -> int:
        self._nrSteps

    def setNrSteps(self, nrSteps: int) -> None:
        self._nrSteps = nrSteps

    def run(self) -> None:
        raise NotImplementedError('Not implemented')