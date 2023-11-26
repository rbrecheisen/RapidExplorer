from PySide6.QtWidgets import QDialog

from plugins.tasks.task import Task


class TaskSettingsDialog(QDialog):
    def __init__(self, task: Task) -> None:
        super(TaskSettingsDialog, self).__init__()
        self._task = task
        # TODO: Get all parameters from the task and build a dialog form
        self._buildTaskSettingsForm(self._task)

    def task(self) -> Task:
        return self._task
    
    def _buildTaskSettingsForm(self, task) -> None:
        pass