from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.copyfilesettask.copyfilesettask import CopyFileSetTask


class CopyFileSetTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CopyFileSetTaskWidget, self).__init__(taskType=CopyFileSetTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass