from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromsegmentationfiletask.createpngfromsegmentationfiletask import CreatePngFromSegmentationFileTask


class CreatePngFromSegmentationFileTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CreatePngFromSegmentationFileTaskWidget, self).__init__(taskType=CreatePngFromSegmentationFileTask)
    
    def validate(self) -> None:
        pass