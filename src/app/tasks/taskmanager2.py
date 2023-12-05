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
        self._tasks = {}
        self._currentTask = None
        self._signal = TaskManagerSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self.loadTasks()

    def signal(self) -> TaskManagerSignal:
        return self._signal

    def loadTasks(self) -> None:
        from tasks.musclefatsegmentationtask.musclefatsegmentationtask import MuscleFatSegmentationTask
        from tasks.bodycompositiontask.bodycompositiontask import BodyCompositionTask
        self._tasks = {
            MuscleFatSegmentationTask.NAME: MuscleFatSegmentationTask(),
            BodyCompositionTask.NAME: BodyCompositionTask(),
        }

    def task(self, name: str) -> Task:
        return self._tasks[name]
    
    def taskNames(self) -> List[str]:
        return self._tasks.keys()
    
    def currentTask(self) -> Task:
        return self._currentTask

    def setCurrentTask(self, task: Task) -> None:
        self._currentTask = task

    def runCurrentTask(self, background: bool=True) -> None:
        self._currentTask.signal().progress.connect(self.taskProgress)
        self._currentTask.signal().finished.connect(self.taskFinished)
        if background:
            QThreadPool.globalInstance().start(self._currentTask)
        else:
            self._currentTask.run()

    def taskProgress(self, progress) -> None:
        self.signal().taskProgress.emit(progress)

    def taskFinished(self, outputFileSet: FileSet) -> None:
        self.signal().taskFinished.emit(outputFileSet)
