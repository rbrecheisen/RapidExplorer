from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QPushButton

from mosamaticdesktop.widgets.dockwidget import DockWidget
from mosamaticdesktop.tasks.taskwidgetmanager import TaskWidgetManager
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._showTaskWidgetButton = None
        self._placeholderWidget = None
        self._taskWidgetManager = TaskWidgetManager()
        self._currentTaskName = None
        self.initUi()

    def initUi(self) -> None:
        self._tasksComboBox = QComboBox(self)
        self._tasksComboBox.addItem(None)
        for taskName in sorted(self._taskWidgetManager.taskNames()):
            self._tasksComboBox.addItem(taskName)
        self._tasksComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        self._showTaskWidgetButton = QPushButton('Show Task Widget')
        self._showTaskWidgetButton.clicked.connect(self.showTaskWidget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self._tasksComboBox)
        layout.addWidget(self._showTaskWidgetButton)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)
        self.setMinimumHeight(200)

    def showTaskWidget(self) -> None:
        if self._currentTaskName:
            taskWidget = self._taskWidgetManager.taskWidget(name=self._currentTaskName)
            taskWidget.show()

    def currentIndexChanged(self, index) -> None:
        taskName = self._tasksComboBox.itemText(index)
        if taskName:
            self._currentTaskName = taskName