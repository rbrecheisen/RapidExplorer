from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromsegmentationfiletask.createpngfromsegmentationfiletask import CreatePngFromSegmentationFileTask


class CreatePngFromSegmentationFileTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CreatePngFromSegmentationFileTaskWidget, self).__init__(taskType=CreatePngFromSegmentationFileTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass