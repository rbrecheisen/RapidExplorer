from PySide6.QtWidgets import QDialog

from app.plugins.tasks.task import Task


class TaskSettingsDialog(QDialog):
    def __init__(self, task: Task) -> None:
        self._task = task

    def task(self) -> Task:
        return self._task