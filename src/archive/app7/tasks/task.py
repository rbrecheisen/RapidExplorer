from typing import Dict

from PySide6.QtCore import QRunnable

from settings.settings import Settings
from data.datamanager import DataManager
from data.fileset import FileSet
from tasks.taskoutput import TaskOutput


class Task(QRunnable):
    NAME = None

    def __init__(self) -> None:
        super(Task, self).__init__()
        self._settings = Settings(name=self.NAME)
        self._dataManager = DataManager()
        self._nrSteps = 0

    def name(self) -> str:
        return self.NAME
    
    def settings(self) -> Settings:
        return self._settings
    
    def setSettings(self, settings: Settings) -> None:
        self._settings = settings

    def dataManager(self) -> DataManager:
        return self._dataManager

    def nrSteps(self) -> int:
        self._nrSteps

    def setNrSteps(self, nrSteps: int) -> None:
        self._nrSteps = nrSteps

    def run(self) -> TaskOutput:
        raise NotImplementedError('Not implemented')