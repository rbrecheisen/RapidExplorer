from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromtagfiletask.createpngfromtagfiletask import CreatePngFromTagFileTask


class CreatePngFromTagFileTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CreatePngFromTagFileTaskWidget, self).__init__(taskType=CreatePngFromTagFileTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass