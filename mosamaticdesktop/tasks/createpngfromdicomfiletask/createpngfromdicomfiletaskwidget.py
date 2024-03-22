from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromdicomfiletask.createpngfromdicomfiletask import CreatePngFromDicomFileTask


class CreatePngFromDicomFileTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CreatePngFromDicomFileTaskWidget, self).__init__(taskType=CreatePngFromDicomFileTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass