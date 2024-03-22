from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.musclefatsegmentationtask.musclefatsegmentationtask import MuscleFatSegmentationTask


class MuscleFatSegmentationTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(MuscleFatSegmentationTaskWidget, self).__init__(taskType=MuscleFatSegmentationTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass