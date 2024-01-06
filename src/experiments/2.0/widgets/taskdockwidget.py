from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QProgressDialog, QCheckBox

from widgets.dockwidget import DockWidget
from tasks.taskwidgetmanager import TaskWidgetManager
from logger import Logger

LOGGER = Logger()


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._placeHolderWidget = None
        self._taskWidgetManager = TaskWidgetManager()
        self.initUi()

    def initUi(self) -> None:
        self._tasksComboBox = QComboBox(self)
        self._tasksComboBox.addItem(None)
        for taskName in self._taskWidgetManager.taskNames():
            self._tasksComboBox.addItem(taskName)
        self._tasksComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        self._placeHolderWidget = QWidget()
        self._placeHolderWidget.setLayout(QVBoxLayout())
        layout = QVBoxLayout()
        layout.addWidget(self._tasksComboBox)
        layout.addWidget(self._placeHolderWidget)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)
        self.setMinimumHeight(200)

    def currentIndexChanged(self, index) -> None:
        if self._placeHolderWidget.layout():
            for i in reversed(range(self._placeHolderWidget.layout().count())): 
                widgetToRemove = self._placeHolderWidget.layout().itemAt(i).widget()
                self._placeHolderWidget.layout().removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
        taskName = self._tasksComboBox.itemText(index)
        if taskName:
            taskWidget = self._taskWidgetManager.taskWidget(name=taskName)
            self._placeHolderWidget.layout().addWidget(taskWidget)