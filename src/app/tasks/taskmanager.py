from typing import List, Dict, Any

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from moduleloader import ModuleLoader
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
        
    def runTask(self, task: Task, background: bool=True) -> None:
        task.signal().progress.connect(self.taskProgress)
        task.signal().finished.connect(self.taskFinished)
        if background:
            QThreadPool.globalInstance().start(task)
        else:
            return task.run()

    def taskProgress(self, progress) -> None:
        self.signal().taskProgress.emit(progress)

    def taskFinished(self, outputFileSetName: str) -> None:
        self.signal().taskFinished.emit(outputFileSetName)