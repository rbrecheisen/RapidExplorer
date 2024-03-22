from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.totalsegmentatortask.totalsegmentatortask import TotalSegmentatorTask


class TotalSegmentatorTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(TotalSegmentatorTaskWidget, self).__init__(taskType=TotalSegmentatorTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass