from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.dummytask.dummytask import DummyTask


class DummyTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(DummyTaskWidget, self).__init__(taskType=DummyTask, progressBar=progressBar)
    
    def validate(self) -> None:
        # self.showValidationError(parameterName='Some parameter', message='Something wrong')
        pass