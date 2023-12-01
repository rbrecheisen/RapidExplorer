from typing import List, Dict, Any

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from moduleloader import ModuleLoader
from data.fileset import FileSet
from tasks.taskmanagersignal import TaskManagerSignal
from tasks.task import Task

SETTINGSFILEPATH = 'settings.ini'


@singleton
class TaskManager:
    def __init__(self) -> None:
        self._tasks = {}
        self._signal = TaskManagerSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self._currentTask = None
        self.loadTasks()

    def tasks(self) -> List[Task]:
        return self._tasks.values()
    
    def signal(self) -> TaskManagerSignal:
        return self._signal
    
    def settings(self) -> QSettings:
        return self._settings
    
    def currentTask(self) -> Task:
        return self._currentTask
    
    def setCurrentTask(self, task: Task) -> None:
        self._currentTask = task
        self.signal().currentTaskChanged.emit(self._currentTask)

    def nrTasks(self) -> int:
        return len(self.tasks())
    
    def task(self, name: str) -> Task:
        return self._tasks[name]
    
    def loadTasks(self) -> Dict[str, Task]:
        self._tasks = ModuleLoader.loadModules(
            moduleDirectoryPath=self.settings().value('tasksDirectoryPath'), moduleBaseClass=Task)
        
    def runCurrentTask(self, background: bool=True) -> None:
        self.currentTask().signal().progress.connect(self.taskProgress)
        self.currentTask().signal().finished.connect(self.taskFinished)
        if background:
            QThreadPool.globalInstance().start(self.currentTask())
        else:
            self.currentTask().run()

    def taskProgress(self, progress) -> None:
        self.signal().taskProgress.emit(progress)

    def taskFinished(self, outputFileSet: FileSet) -> None:
        self.currentTask().signal().progress.disconnect(self.taskProgress)
        self.currentTask().signal().finished.disconnect(self.taskFinished)
        self.signal().taskFinished.emit(outputFileSet)