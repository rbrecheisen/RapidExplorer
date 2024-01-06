from tasks.taskwidget import TaskWidget
from tasks.dummytask.dummytask import DummyTask


class DummyTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(DummyTaskWidget, self).__init__(taskType=DummyTask)
        
        self.addIntegerParameter(
            name='nrIterations', 
            labelText='Nr. Iterations',
            optional=False,
            visible=True,
            defaultValue=10,
        )