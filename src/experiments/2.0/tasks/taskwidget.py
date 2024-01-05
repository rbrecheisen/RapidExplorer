from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout

from tasks.task import Task


class TaskWidget(QWidget):
    def __init__(self) -> None:
        super(TaskWidget, self).__init__()

    def startTask(self) -> None:
        raise NotImplementedError()
    
    def cancelTask(self) -> None:
        raise NotImplementedError()