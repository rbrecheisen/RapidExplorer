from PySide6.QtWidgets import QDialog

from plugins.tasks.task import Task


class TaskSettingsDialog(QDialog):
    def __init__(self, task: Task) -> None:
        super(TaskSettingsDialog, self).__init__()
        self._task = task

    def task(self) -> Task:
        return self._task