from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout

from tasks.task import Task


class TaskWidget(QWidget):
    def __init__(self, task: Task) -> None:
        super(TaskWidget, self).__init__()
        self._task = task

    def startTask(self) -> None:
        self._task.start()

    def cancelTask(self) -> None:
        self._task.cancel()

    def taskStatus(self) -> int:
        return self._task.status()