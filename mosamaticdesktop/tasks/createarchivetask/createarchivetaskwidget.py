from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createarchivetask.createarchivetask import CreateArchiveTask


class CreateArchiveTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CreateArchiveTaskWidget, self).__init__(taskType=CreateArchiveTask)
    
    def validate(self) -> None:
        pass