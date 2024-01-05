import os

from typing import Dict

from tasks.taskwidget import TaskWidget
from tasks.task import Task
from utils import ModuleLoader


class TaskManager:
    def __init__(self) -> None:
        self._tasks = self.loadTasks()
        print(self._tasks['DummyTask']().name())
        self._taskWidgets = self.loadTaskWidgets()

    def loadTasks(self):
        classes = ModuleLoader.loadModuleClasses(
            moduleDirectoryPath=os.path.dirname(os.path.realpath(__file__)),
            moduleBaseClass=Task,
            fileNameEndsWith='task.py',
        )
        return classes

    def loadTaskWidgets(self):
        classes = ModuleLoader.loadModuleClasses(
            moduleDirectoryPath=os.path.dirname(os.path.realpath(__file__)),
            moduleBaseClass=TaskWidget,
            fileNameEndsWith='taskwidget.py',
        )
        return classes