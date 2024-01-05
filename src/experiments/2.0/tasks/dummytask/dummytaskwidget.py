from PySide6.QtWidgets import QPushButton, QVBoxLayout

from tasks.taskwidget import TaskWidget
from tasks.dummytask.dummytask import DummyTask


class DummyTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(DummyTaskWidget, self).__init__(DummyTask())
        button = QPushButton('Hello!')
        layout = QVBoxLayout()
        layout.addWidget(button)
        self.setLayout(layout)
