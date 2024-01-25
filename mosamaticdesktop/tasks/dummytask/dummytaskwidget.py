from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.dummytask.dummytask import DummyTask


class DummyTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(DummyTaskWidget, self).__init__(taskType=DummyTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='This is some description of the dummy task'
        )
        self.addIntegerParameter(
            name='nrIterations', 
            labelText='Nr. Iterations',
            optional=False,
            visible=True,
            defaultValue=10,
            minimum=0,
            maximum=100,
            step=1,
        )
    
    def validate(self) -> None:
        # self.showValidationError(parameterName='Some parameter', message='Something wrong')
        pass