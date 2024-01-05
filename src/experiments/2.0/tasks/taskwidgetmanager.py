import os
import json

from typing import List

from tasks.taskwidget import TaskWidget
from utils import ModuleLoader


class TaskWidgetManager:
    def __init__(self) -> None:
        self._taskWidgets = self.loadTaskWidgets()
        print(self._taskWidgets)

    def taskNames(self) -> List[str]:
        return list(self._taskWidgets.keys())
    
    def createTaskWidget(self, name) -> TaskWidget:
        return self._taskWidgets[name]()

    def loadTaskWidgets(self):
        taskWidgets = ModuleLoader.loadModuleClasses(
            moduleDirectoryPath=os.path.dirname(os.path.realpath(__file__)),
            moduleBaseClass=TaskWidget,
            fileNameEndsWith='taskwidget.py',
        )
        return taskWidgets