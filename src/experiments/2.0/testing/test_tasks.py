import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from tasks.task import Task
from tasks.dummytask.dummytaskwidget import DummyTaskWidget

# button = widget.findChild(QPushButton, 'taskWidgetButton')
# qtbot.addWidget(widget)
# qtbot.mouseClick(button, Qt.LeftButton)


def test_taskWidgetCanStartAndCancelTask(qtbot):
    widget = DummyTaskWidget()
    widget.startTask()
    assert widget.taskStatus() == Task.RUNNING
    time.sleep(5)
    widget.cancelTask()
    assert widget.taskStatus() == Task.CANCELLING or widget.taskStatus() == Task.CANCELED
