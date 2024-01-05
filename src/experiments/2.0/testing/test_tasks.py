import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from tasks.task import Task
from tasks.dummytask.dummytaskwidget import DummyTaskWidget

# button = widget.findChild(QPushButton, 'taskWidgetButton')
# qtbot.addWidget(widget)
# qtbot.mouseClick(button, Qt.LeftButton)


def test_taskWidgetCanStartTask(qtbot):
    widget = DummyTaskWidget()
    widget.startTask()
    assert widget.taskStatus() == Task.FINISHED


def test_taskWidgetCanStartAndCancelTask():
    widget = DummyTaskWidget()
    widget.startTask()

    # Task first finishes above statement before it gets to the cancelTask()
    # Need to implement threading!

    time.sleep(5)
    widget.cancelTask()
    assert widget.taskStatus() == Task.CANCELED
