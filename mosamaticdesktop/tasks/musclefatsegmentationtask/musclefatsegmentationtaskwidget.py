from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.musclefatsegmentationtask.musclefatsegmentationtask import MuscleFatSegmentationTask


class MuscleFatSegmentationTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(MuscleFatSegmentationTaskWidget, self).__init__(taskType=MuscleFatSegmentationTask)
    
    def validate(self) -> None:
        pass