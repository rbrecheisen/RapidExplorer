from PySide6.QtCore import QObject, Signal

from tasks.task import Task


class TaskManagerSignal(QObject):
    currentTaskChanged = Signal(Task)