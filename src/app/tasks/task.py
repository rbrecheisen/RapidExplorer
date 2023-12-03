from typing import Dict

from PySide6.QtCore import QRunnable

from tasks.tasksettings import TaskSettings
from data.datamanager import DataManager
from data.fileset import FileSet

"""
Base task for running processing operations on file sets. Each derived task should do
the following:

(1)  Define its setting types (constructor)
(2)  Implement mandatory outputFileSet() method which retrieves output file set from settings
(3)  Collect input data and settings
(4)  Create output file set directory as given by settings
(5)  Determine output file set name
(6)  Calculate number of steps required to complete processing (#files in input data)
(7)  Execute processing
(8)  Create/building output file set
(9)  Adding output file set name to task settings
(10) Implement methods for emitting signals about task progress and finish
"""


class Task(QRunnable):
    NAME = None

    def __init__(self, name: str=None) -> None:
        super(Task, self).__init__()
        # self._name = name
        self._settings = TaskSettings(taskName=self.NAME)
        self._dataManager = DataManager()
        self._nrSteps = 0
        # self._outputFileSet = None

    def name(self) -> str:
        # return self._name
        return self.NAME
    
    def settings(self) -> TaskSettings:
        return self._settings
    
    def setSettings(self, settings: TaskSettings) -> None:
        self._settings = settings

    def dataManager(self) -> DataManager:
        return self._dataManager

    def nrSteps(self) -> int:
        self._nrSteps

    def setNrSteps(self, nrSteps: int) -> None:
        self._nrSteps = nrSteps

    # def outputFileSet(self) -> FileSet:
    #     return self._outputFileSet
    
    # def setOutputFileSet(self, outputFileSet: FileSet) -> None:
    #     self._outputFileSet = outputFileSet

    def run(self) -> FileSet:
        raise NotImplementedError('Not implemented')