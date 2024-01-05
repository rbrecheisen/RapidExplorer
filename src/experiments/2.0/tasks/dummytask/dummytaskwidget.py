from tasks.taskwidget import TaskWidget
from tasks.dummytask.dummytask import DummyTask


class DummyTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(DummyTaskWidget, self).__init__(DummyTask())
