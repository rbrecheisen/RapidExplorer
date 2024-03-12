import os

from PySide6.QtWidgets import QProgressBar

from typing import List, Dict

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.utils import ModuleLoader
from mosamaticdesktop.singleton import singleton
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


@singleton
class TaskWidgetManager:
    def __init__(self, progressBar: QProgressBar) -> None:
        self._progressBar = progressBar
        self._taskWidgetTypes = self.loadTaskWidgetTypes()
        self._taskTypes = self.loadTaskTypes()
        self._taskWidgets = {}
        self._tasks = {}

    def taskNames(self) -> List[str]:
        return list(self._taskTypes.keys())
    
    def taskWidgets(self) -> Dict[str, TaskWidget]:
        return self._taskWidgets
    
    def tasks(self) -> Dict[str, Task]:
        return self._tasks
    
    def taskWidget(self, name) -> TaskWidget:
        if name in self._taskWidgetTypes.keys():
            if name not in self._taskWidgets.keys():
                self._taskWidgets[name] = self._taskWidgetTypes[name](progressBar=self._progressBar)
            return self._taskWidgets[name]
        LOGGER.error(f'TaskWidgetManager: task widget for task {name} does not exist')
        return None
    
    def task(self, name) -> Task:
        if name in self._taskTypes.keys():
            if name not in self._tasks.keys():
                self._tasks[name] = self._taskTypes[name]()
            return self._tasks[name]
        LOGGER.error(f'TaskWidgetManager: task {name} does not exist')
        return None
    
    def loadTaskTypes(self):
        moduleDirectoryPath = os.path.dirname(os.path.realpath(__file__))
        LOGGER.info(f'TaskWidgetManager: loading tasks from {moduleDirectoryPath}...')
        taskWidgets = ModuleLoader.loadModuleClasses(
            moduleDirectoryPath=moduleDirectoryPath,
            moduleBaseClass=Task,
            fileNameEndsWith='task.py',
        )
        for taskName in taskWidgets.keys():
            LOGGER.info(f'TaskWidgetManager: Loaded task type {taskName}')
        return taskWidgets        

    def loadTaskWidgetTypes(self):
        moduleDirectoryPath = os.path.dirname(os.path.realpath(__file__))
        LOGGER.info(f'TaskWidgetManager: loading task widget types from {moduleDirectoryPath}...')
        taskWidgets = ModuleLoader.loadModuleClasses(
            moduleDirectoryPath=moduleDirectoryPath,
            moduleBaseClass=TaskWidget,
            fileNameEndsWith='taskwidget.py',
        )
        return taskWidgets