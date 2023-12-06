import os

from typing import List

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from data.fileset import FileSet
from tasks.taskmanagersignal import TaskManagerSignal
from tasks.task import Task

SETTINGSFILEPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


@singleton
class TaskManager:
    def __init__(self) -> None:
        self._taskTypes = {}
        self._signal = TaskManagerSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self.loadTaskTypes()

    def signal(self) -> TaskManagerSignal:
        return self._signal

    def loadTaskTypes(self) -> None:
        from tasks.musclefatsegmentationtask.musclefatsegmentationtask import MuscleFatSegmentationTask
        from tasks.bodycompositiontask.bodycompositiontask import BodyCompositionTask
        from tasks.createarchivetask.createarchivetask import CreateArchiveTask
        self._taskTypes = {
            MuscleFatSegmentationTask.NAME: MuscleFatSegmentationTask,
            BodyCompositionTask.NAME: BodyCompositionTask,
        }

    def taskTypes(self) -> List[Task]:
        return self._taskTypes

    def taskTypeNames(self) -> List[str]:
        return self._taskTypes.keys()
    
    def createTaskFromTaskTypeName(self, name: str) -> Task:
        return self._taskTypes[name]()
    
    def runTask(self, task: Task, background=True) -> None:
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
