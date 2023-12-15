import os

from typing import List

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from logger import Logger
from tasks.tasksignal import TaskSignal
from tasks.task import Task
from tasks.taskoutput import TaskOutput
from utils import SettingsIniFile

SETTINGSFILEPATH = SettingsIniFile().path()

LOGGER = Logger()


@singleton
class TaskManager:
    def __init__(self) -> None:
        self._taskTypes = {}
        self._signal = TaskSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self.loadTaskTypes()

    def signal(self) -> TaskSignal:
        return self._signal

    def loadTaskTypes(self) -> None:
        from tasks.bodycompositiontask.bodycompositiontask import BodyCompositionTask
        from tasks.checkdicomheaderstask.checkdicomheaderstask import CheckDicomHeadersTask
        from tasks.createarchivetask.createarchivetask import CreateArchiveTask
        from tasks.createpngsfrommusclefatsegmentationtask.createpngsfrommusclefatsegmentationtask import CreatePngsFromMuscleFatSegmentationTask
        from tasks.musclefatsegmentationtask.musclefatsegmentationtask import MuscleFatSegmentationTask        
        self._taskTypes = {
            BodyCompositionTask.NAME: BodyCompositionTask,
            CheckDicomHeadersTask.NAME: CheckDicomHeadersTask,
            CreateArchiveTask.NAME: CreateArchiveTask,
            CreatePngsFromMuscleFatSegmentationTask.NAME: CreatePngsFromMuscleFatSegmentationTask,
            MuscleFatSegmentationTask.NAME: MuscleFatSegmentationTask,
        }
        for k in self._taskTypes.keys():
            LOGGER.info(f'Loaded task {k}')

    def taskTypes(self) -> List[Task]:
        return self._taskTypes

    def taskTypeNames(self) -> List[str]:
        return self._taskTypes.keys()
    
    def createTaskFromTaskTypeName(self, name: str) -> Task:
        return self._taskTypes[name]()
    
    def runTask(self, task: Task, background=True) -> None:
        background = False
        LOGGER.info(f'Running task {task.name()} with background={background}')
        task.signal().progress.connect(self.taskProgress)
        task.signal().finished.connect(self.taskFinished)
        if background:
            QThreadPool.globalInstance().start(task)
        else:
            task.run()
    
    def taskProgress(self, progress) -> None:
        self.signal().progress.emit(progress)

    def taskFinished(self, taskOutput: TaskOutput) -> None:
        LOGGER.info(f'TaskManager.taskFinished() taskOutput={taskOutput}')
        self.signal().finished.emit(taskOutput)
