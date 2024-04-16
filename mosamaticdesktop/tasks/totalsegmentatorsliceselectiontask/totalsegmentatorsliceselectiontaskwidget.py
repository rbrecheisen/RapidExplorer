from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.totalsegmentatorsliceselectiontask.totalsegmentatorsliceselectiontask import TotalSegmentatorSliceSelectionTask


class TotalSegmentatorSliceSelectionTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(TotalSegmentatorSliceSelectionTaskWidget, self).__init__(taskType=TotalSegmentatorSliceSelectionTask)
    
    def validate(self) -> None:
        pass