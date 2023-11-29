from PySide6.QtWidgets import QDialog


class TaskSettingsDialog(QDialog):
    def __init__(self, task: Task) -> None:
        super(TaskSettingsDialog, self).__init__()
        self._task = task
        self._formFieldWidgets = {}
        self.initUi()

    def initUi(self) -> None:
        pass