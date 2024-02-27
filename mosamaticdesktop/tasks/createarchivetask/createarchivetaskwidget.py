from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createarchivetask.createarchivetask import CreateArchiveTask


class CreateArchiveTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CreateArchiveTaskWidget, self).__init__(taskType=CreateArchiveTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass