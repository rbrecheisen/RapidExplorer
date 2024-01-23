import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from tasks.dummytask.dummytaskwidget import DummyTaskWidget


def test_taskWidgetCanStartAndCancelTask(qtbot):
    widget = DummyTaskWidget()
    widget.setTest(True)
    qtbot.addWidget(widget)
    # Start task
    startButton = widget.findChild(QPushButton, 'startButton')
    qtbot.mouseClick(startButton, Qt.LeftButton)
    assert widget.taskIsRunning()
    # Check progress
    time.sleep(5)
    # Cancel task
    cancelButton = widget.findChild(QPushButton, 'cancelButton')
    qtbot.mouseClick(cancelButton, Qt.LeftButton)
    assert widget.taskIsCanceling() or widget.taskIsCanceled()