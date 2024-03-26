from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromdicomfiletask.createpngfromdicomfiletask import CreatePngFromDicomFileTask


class CreatePngFromDicomFileTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CreatePngFromDicomFileTaskWidget, self).__init__(taskType=CreatePngFromDicomFileTask)
    
    def validate(self) -> None:
        pass