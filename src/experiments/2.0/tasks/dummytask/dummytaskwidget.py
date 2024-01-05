from tasks.taskwidget import TaskWidget
from tasks.dummytask.dummytask import DummyTask


class DummyTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(DummyTaskWidget, self).__init__()
        self._task = DummyTask()

    def startTask(self) -> None:
        self._task.start()

    def cancelTask(self) -> None:
        self._task.cancel()

    def taskStatus(self) -> int:
        return self._task.status()