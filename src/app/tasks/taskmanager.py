import os

from typing import List

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from data.fileset import FileSet
from tasks.taskmanagersignal import TaskManagerSignal
from tasks.task import Task
from settings.settings import Settings

SETTINGSFILEPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


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
        self.signal().currentTaskChanged.emit(self._currentTaskDefinitionName)

    def nrTaskDefinitions(self) -> int:
        return len(self._taskDefinitions.keys())
    
    def taskSettings(self, name: str) -> Settings:
        return self._taskSettings[name]
    
    def updateTaskSettings(self, name: str, taskSettings: Settings) -> None:
        self._taskSettings[name] = taskSettings

    def currentTaskSettings(self) -> Settings:
        return self._taskSettings[self.currentTaskDefinitionName()]
    
    def loadTaskDefinitionsAndSettings(self):
        # Loading task definitions by importing them explicitly. Loading from file doesn't work
        # after compilation with Nuitka
        from tasks.musclefatsegmentationtask.musclefatsegmentationtask import MuscleFatSegmentationTask
        from tasks.bodycompositiontask.bodycompositiontask import BodyCompositionTask
        self._taskDefinitions = {
            MuscleFatSegmentationTask.NAME: MuscleFatSegmentationTask,
            BodyCompositionTask.NAME: BodyCompositionTask,
        }
        # self._taskDefinitions = ModuleLoader.loadModuleClasses(moduleDirectoryPath=self._tasksDirectoryPath, moduleBaseClass=Task)
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