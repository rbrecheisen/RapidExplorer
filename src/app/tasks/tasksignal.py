from PySide6.QtCore import QObject, Signal


class TaskSignal(QObject):
    progress = Signal(int)
    finished = Signal(bool)