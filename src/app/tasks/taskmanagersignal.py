from PySide6.QtCore import QObject, Signal

from tasks.task import Task
from data.fileset import FileSet


class TaskManagerSignal(QObject):
    currentTaskChanged = Signal(Task)
    taskProgress = Signal(int)
    taskFinished = Signal(FileSet)