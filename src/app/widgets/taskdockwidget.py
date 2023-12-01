from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QProgressDialog

from widgets.dockwidget import DockWidget
from widgets.tasksettingsdialog import TaskSettingsDialog
from tasks.taskmanager import TaskManager
from tasks.taskmanagersignal import TaskManagerSignal
from tasks.task import Task


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._showSettingsDialogButton = None
        self._runSelectedTaskButton = None
        self._progressBarDialog = None
        self._taskManager = None
        self._signal = TaskManagerSignal()
        self.initTaskManager()
        self.initUi()
        self.loadTasks()

    def signal(self) -> TaskManagerSignal:
        return self._signal
    
    def initTaskManager(self) -> None:
        self._taskManager = TaskManager()
        self._taskManager.signal().taskProgress.connect(self.taskProgress)
        self._taskManager.signal().taskFinished.connect(self.taskFinished)

    def initUi(self) -> None:
        self._tasksComboBox = QComboBox(self)
        self._tasksComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        self._showSettingsDialogButton = QPushButton('Edit Settings...')
        self._showSettingsDialogButton.setFixedWidth(200)
        self._showSettingsDialogButton.setEnabled(False)
        self._showSettingsDialogButton.clicked.connect(self.showSettingsDialog)
        self._runSelectedTaskButton = QPushButton('Run Task')
        self._runSelectedTaskButton.clicked.connect(self.runSelectedTask)
        self._runSelectedTaskButton.setEnabled(False)
        self.initProgressBarDialog()
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._showSettingsDialogButton)
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

    def initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Running Task...', 'Abort', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def currentIndexChanged(self, index) -> None:
        taskName = self._tasksComboBox.itemText(index)
        if taskName:
            self._showSettingsDialogButton.setEnabled(True)
            self._taskManager.setCurrentTask(self._taskManager.task(taskName))
        else:
            self._showSettingsDialogButton.setEnabled(False)

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
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            # self._taskManager.signal().taskProgress.connect(self.taskProgress)
            # self._taskManager.signal().taskFinished.connect(self.taskFinished)
            task = self._taskManager.task(taskName)
            self._taskManager.runTask(task)

    def loadTasks(self) -> None:
        self._tasksComboBox.clear()
        self._tasksComboBox.addItem(None)
        for task in self._taskManager.tasks():
            self._tasksComboBox.addItem(task.name())

    def taskProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)

    def taskFinished(self, task: Task) -> None:
        # self._taskManager.signal().taskProgress.disconnect(self.taskProgress)
        # self._taskManager.signal().taskFinished.disconnect(self.taskFinished)
        self._signal.taskFinished.emit(task)