from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromtagfiletask.createpngfromtagfiletask import CreatePngFromTagFileTask


class CreatePngFromTagFileTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CreatePngFromTagFileTaskWidget, self).__init__(taskType=CreatePngFromTagFileTask)
    
    def validate(self) -> None:
        pass