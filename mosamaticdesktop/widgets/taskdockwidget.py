from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QProgressBar

from mosamaticdesktop.widgets.dockwidget import DockWidget
from mosamaticdesktop.tasks.taskwidgetmanager import TaskWidgetManager
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class TaskDockWidget(DockWidget):
    def __init__(self, title: str, progressBar: QProgressBar) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._placeholderWidget = None
        self._taskWidgetManager = TaskWidgetManager(progressBar=progressBar)
        self.initUi()

    def initUi(self) -> None:
        self._tasksComboBox = QComboBox(self)
        self._tasksComboBox.addItem(None)
        for taskName in sorted(self._taskWidgetManager.taskNames()):
            self._tasksComboBox.addItem(taskName)
        self._tasksComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        self._placeholderWidget = QWidget()
        self._placeholderWidget.setLayout(QVBoxLayout())
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self._tasksComboBox)
        layout.addWidget(self._placeholderWidget)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)
        self.setMinimumHeight(200)

    def currentIndexChanged(self, index) -> None:
        if self._placeholderWidget.layout():
            for i in reversed(range(self._placeholderWidget.layout().count())): 
                widgetToRemove = self._placeholderWidget.layout().itemAt(i).widget()
                self._placeholderWidget.layout().removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
        taskName = self._tasksComboBox.itemText(index)
        if taskName:
            taskWidget = self._taskWidgetManager.taskWidget(name=taskName)
            self._placeholderWidget.layout().addWidget(taskWidget)
