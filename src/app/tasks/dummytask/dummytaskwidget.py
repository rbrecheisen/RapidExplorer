from tasks.taskwidget import TaskWidget
from tasks.dummytask.dummytask import DummyTask


class DummyTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(DummyTaskWidget, self).__init__(taskType=DummyTask)
        # self._inputFileSet = self.addFileSetParameter(labelText='Input File Set')
        # self._outputFileSetPath = self.addPathParameter(labelText='Output File Set Path')
        # self._outputFileSetName = self.addTextParameter(labelText='Output File Set Name')
        self.addIntegerParameter(
            name='nrIterations', 
            labelText='Nr. Iterations',
            optional=False,
            visible=True,
            defaultValue=10,
        )