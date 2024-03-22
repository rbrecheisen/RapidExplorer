import os

from typing import List, Dict

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.utils import ModuleLoader
from mosamaticdesktop.singleton import singleton
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


@singleton
class TaskWidgetManager:
    def __init__(self) -> None:
        self._taskWidgetTypes = self.loadTaskWidgetTypes()
        self._taskWidgets = {}

    def taskNames(self) -> List[str]:
        return list(self._taskWidgetTypes.keys())
    
    def taskWidgets(self) -> Dict[str, TaskWidget]:
        return self._taskWidgets
    
    def taskWidget(self, name) -> TaskWidget:
        if name in self._taskWidgetTypes.keys():
            if name not in self._taskWidgets.keys():
                self._taskWidgets[name] = self._taskWidgetTypes[name]()
            return self._taskWidgets[name]
        LOGGER.error(f'TaskWidgetManager: task widget for task {name} does not exist')
        return None
    
    def loadTaskWidgetTypes(self):
        moduleDirectoryPath = os.path.dirname(os.path.realpath(__file__))
        LOGGER.info(f'TaskWidgetManager: loading task widget types from {moduleDirectoryPath}...')
        taskWidgets = ModuleLoader.loadModuleClasses(
            moduleDirectoryPath=moduleDirectoryPath,
            moduleBaseClass=TaskWidget,
            fileNameEndsWith='taskwidget.py',
        )
        return taskWidgets