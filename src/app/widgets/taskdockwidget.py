from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog

from widgets.dockwidget import DockWidget
from widgets.tasksettingsdialog import TaskSettingsDialog
from tasks.taskmanager import TaskManager


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._runSelectedTaskButton = None
        self._taskManager = TaskManager()
        self.initUi()
        self.loadTasks()

    def initUi(self) -> None:
        self._tasksComboBox = QComboBox(self)
        self._tasksComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        showSettingsDialogButton = QPushButton('Edit Settings...')
        showSettingsDialogButton.setFixedWidth(200)
        showSettingsDialogButton.clicked.connect(self.showSettingsDialog)
        self._runSelectedTaskButton = QPushButton('Run Task')
        self._runSelectedTaskButton.clicked.connect(self.runSelectedTask)
        self._runSelectedTaskButton.setEnabled(False)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(showSettingsDialogButton)
        buttonLayout.addWidget(self._runSelectedTaskButton)
        buttonLayout.setAlignment(Qt.AlignRight)
        buttonWidget = QWidget()
        buttonWidget.setLayout(buttonLayout)
        layout = QVBoxLayout()
        layout.addWidget(self._tasksComboBox)
        layout.addWidget(buttonWidget)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)
        self.setMinimumHeight(200)

    def currentIndexChanged(self, index) -> None:
        taskName = self._tasksComboBox.itemText(index)
        if taskName:
            self._taskManager.setCurrentTask(self._taskManager.task(taskName))

    def showSettingsDialog(self) -> None:
        taskName = self._tasksComboBox.currentText()
        if taskName:
            settingsDialog = TaskSettingsDialog(self._taskManager.task(taskName))
            resultCode = settingsDialog.show()
            if resultCode == QDialog.Accepted:
                self._runSelectedTaskButton.setEnabled(True)

    def runSelectedTask(self) -> None:
        taskName = self._tasksComboBox.currentText()
        if taskName:
            self._taskManager.runTask(self._taskManager.task(taskName))

    def loadTasks(self) -> None:
        self._tasksComboBox.clear()
        self._tasksComboBox.addItem(None)
        for task in self._taskManager.tasks():
            self._tasksComboBox.addItem(task.name())