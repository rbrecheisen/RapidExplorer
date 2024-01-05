from PySide6.QtWidgets import QWidget

from tasks.task import Task


class TaskWidget(QWidget):    
    # Trick to return the child class name when NAME is retrieved
    # https://chat.openai.com/c/b7bd6334-5ec3-40e3-9af1-93405c68d795
    @classmethod
    def NAME(cls):
        return cls.__qualname__[:-6]
    
    def __init__(self, task: Task) -> None:
        super(TaskWidget, self).__init__()
        self._task = task

    def name(self) -> str:
        return self.__class__.__name__

    def startTask(self) -> None:
        self._task.start()

    def cancelTask(self) -> None:
        self._task.cancel()

    def taskStatus(self) -> int:
        return self._task.status()