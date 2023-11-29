import os
import importlib

from typing import List, Dict

from PySide6.QtCore import QSettings

from singleton import singleton
from tasks.taskmanagersignal import TaskManagerSignal
from tasks.task import Task

SETTINGSFILEPATH = 'settings.ini'


@singleton
class TaskManager:  # Inherits from generalized object manager parsing Python packages?
    def __init__(self) -> None:
        self._tasks = {}
        self._currentTask = None
        self._signal = TaskManagerSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)

    def tasks(self) -> List[Task]:
        return self._tasks.values()
    
    def nrTasks(self) -> int:
        return len(self.tasks())
    
    def currentTask(self) -> Task:
        return self._currentTask
    
    def signal(self) -> TaskManagerSignal:
        return self._signal
    
    def settings(self) -> QSettings:
        return self._settings
    
    def task(self, name: str) -> Task:
        return self._tasks[name]
    
    def setCurrentTask(self, task: Task) -> None:
        self._currentTask = task
        self.signal().currentTaskChanged.emit(self._currentTask)

    def loadTasks(self) -> Dict[str, Task]:
        for root, dirs, files in os.walk(self.settings().value('taskDirectory')):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                if fileName == '__init__.py':
                    taskModule = filePath.split(os.path.sep)[-2]
                    if taskModule != 'tasks':
                        spec = importlib.util.spec_from_file_location(taskModule, filePath)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            for attributeName in dir(module):
                                attribute = getattr(module, attributeName)
                                if isinstance(attribute, type) and issubclass(attribute, Task) and attribute is not Task:
                                    task = attribute()
                                    self._tasks[task.name()] = task