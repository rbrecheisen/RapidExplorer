from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.findscanstask.findscanstask import FindScansTask


class FindScansTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(FindScansTaskWidget, self).__init__(taskType=FindScansTask)
    
    def validate(self) -> None:
        pass