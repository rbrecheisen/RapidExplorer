import time

from PySide6.QtCore import QObject, QRunnable, Signal

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class TaskProgressMonitor(QRunnable, QObject):
    class TaskProgressSignal(QObject):
        progress = Signal(int)
        finished = Signal(bool)

    def __init__(self, task: Task, progress, finished) -> None:
        super(TaskProgressMonitor, self).__init__()
        self._task = task
        self._signal = self.TaskProgressSignal()
        self._signal.progress.connect(progress)
        self._signal.finished.connect(finished)

    def signal(self):
        return self._signal

    def run(self) -> None:
        while True:
            if self._task.statusIsRunning():
                progress = self._task.progress()
                self._signal.progress.emit(progress)
            else:
                self._signal.finished.emit(True)
                break