from PySide6.QtCore import QObject, Signal

# from tasks.task import Task
from data.fileset import FileSet


class TaskSignal(QObject):
    progress = Signal(int)
    finished = Signal(FileSet)