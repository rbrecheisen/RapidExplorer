from typing import List

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from moduleloader import ModuleLoader
from data.fileset import FileSet
from tasks.taskmanagersignal import TaskManagerSignal
from tasks.task import Task
from tasks.tasksettings import TaskSettings

SETTINGSFILEPATH = 'settings.ini'


@singleton
class TaskManager:
    def __init__(self) -> None:
        self._taskDefinitions = {}
        self._taskSettings = {}
        self._signal = TaskManagerSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self._currentTaskDefinitionName = None
        self._currentTaskSettings = None
        self.loadTaskDefinitionsAndSettings()

    def tasks(self) -> List[Task]:
        return self._tasks.values()
    
    def taskDefinitions(self) -> List[Task]:
        return self._taskDefinitions.values()
    
    def taskDefinitionNames(self) -> List[str]:
        return self._taskDefinitions.keys()
    
    def signal(self) -> TaskManagerSignal:
        return self._signal
    
    def settings(self) -> QSettings:
        return self._settings
    
    def taskDefinition(self, name: str) -> Task:
        return self._taskDefinitions[name]
    
    def currentTaskDefinitionName(self) -> str:
        return self._currentTaskDefinitionName
    
    def setCurrentTaskDefinitionName(self, currentTaskDefinitionName: str) -> None:
        if currentTaskDefinitionName not in self._taskDefinitions.keys():
            raise RuntimeError(f'Class definition for task {currentTaskDefinitionName} does not exist')
        self._currentTaskDefinitionName = currentTaskDefinitionName

    def nrTaskDefinitions(self) -> int:
        return len(self._taskDefinitions.keys())
    
    def taskSettings(self, name: str) -> TaskSettings:
        return self._taskSettings[name]
    
    def updateTaskSettings(self, name: str, taskSettings: TaskSettings) -> None:
        self._taskSettings[name] = taskSettings

    def currentTaskSettings(self) -> TaskSettings:
        return self._taskSettings[self.currentTaskDefinitionName()]
    
    def loadTaskDefinitionsAndSettings(self):
        self._taskDefinitions = ModuleLoader.loadModuleClasses(
            moduleDirectoryPath=self.settings().value('tasksDirectoryPath'), moduleBaseClass=Task)
        self._taskSettings = {}
        for taskDefinitionName in self._taskDefinitions.keys():
            taskDefinition = self._taskDefinitions[taskDefinitionName]
            task = taskDefinition()
            taskSettings = task.settings()
            self._taskSettings[taskDefinitionName] = taskSettings

    def createTask(self, name: str) -> Task:
        taskDefinition = self._taskDefinitions[name]
        task = taskDefinition()
        return task
        
    def runCurrentTask(self, background: bool=True) -> None:
        task = self.createTask(self.currentTaskDefinitionName())
        task.setSettings(self.currentTaskSettings())
        task.signal().progress.connect(self.taskProgress)
        task.signal().finished.connect(self.taskFinished)
        if background:
            QThreadPool.globalInstance().start(task)
        else:
            task.run()

    def taskProgress(self, progress) -> None:
        self.signal().taskProgress.emit(progress)

    def taskFinished(self, outputFileSet: FileSet) -> None:
        self.signal().taskFinished.emit(outputFileSet)