from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.totalsegmentatortask.totalsegmentatortask import TotalSegmentatorTask


class TotalSegmentatorTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(TotalSegmentatorTaskWidget, self).__init__(taskType=TotalSegmentatorTask)
    
    def validate(self) -> None:
        pass