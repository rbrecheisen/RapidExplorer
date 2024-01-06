from PySide6.QtCore import QObject, Signal

from tasks.taskoutput import TaskOutput


class TaskSignal(QObject):
    progress = Signal(int)
    finished = Signal(TaskOutput)