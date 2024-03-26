from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.copyfilesettask.copyfilesettask import CopyFileSetTask


class CopyFileSetTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CopyFileSetTaskWidget, self).__init__(taskType=CopyFileSetTask)
    
    def validate(self) -> None:
        pass