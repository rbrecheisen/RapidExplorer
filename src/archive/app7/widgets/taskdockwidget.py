from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QProgressDialog, QCheckBox

from widgets.dockwidget import DockWidget
from widgets.tasksettingsdialog import TaskSettingsDialog
from tasks.taskmanager import TaskManager
from tasks.tasksignal import TaskSignal
from tasks.taskoutput import TaskOutput
from logger import Logger

LOGGER = Logger()


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._showSettingsDialogButton = None
        self._runSelectedTaskButton = None
        self._runInBackgroundCheckBox = None
        self._progressBarDialog = None
        self._taskManager = None
        self._signal = TaskSignal()
        self.initTaskManager()
        self.initUi()
        self.loadTaskNames()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def initTaskManager(self) -> None:
        self._taskManager = TaskManager()
        self._taskManager.signal().progress.connect(self.taskProgress)
        self._taskManager.signal().finished.connect(self.taskFinished)

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
        self._runInBackgroundCheckBox = QCheckBox('Run in Background', self)
        self._runInBackgroundCheckBox.setChecked(True)
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
        layout.addWidget(self._runInBackgroundCheckBox)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)
        self.setMinimumHeight(200)

    def initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Running task...', 'Abort', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def currentIndexChanged(self, index) -> None:
        taskName = self._tasksComboBox.itemText(index)
        if taskName:
            self._showSettingsDialogButton.setEnabled(True)
            LOGGER.info(f'TaskDockWidget.currentIndexChanged() Creating new task instance: {taskName}')
            self._currentTask = self._taskManager.createTaskFromTaskTypeName(name=taskName)
        else:
            self._showSettingsDialogButton.setEnabled(False)
            self._runSelectedTaskButton.setEnabled(False)
            self._currentTask = None

    def showSettingsDialog(self) -> None:
        taskName = self._tasksComboBox.currentText()
        if taskName:
            LOGGER.info(f'TaskDockWidget.showSettingsDialog() currentTask={self._currentTask}')
            if not self._currentTask:
                LOGGER.info(f'TaskDockWidget.showSettingsDialog() Creating new task instance for: {taskName}')
                self._currentTask = self._taskManager.createTaskFromTaskTypeName(name=taskName)
            settingsDialog = TaskSettingsDialog(self._currentTask.settings())
            resultCode = settingsDialog.show()
            if resultCode == QDialog.Accepted:
                self._runSelectedTaskButton.setEnabled(True)
                self._runSelectedTaskButton.setFocus()

    def runSelectedTask(self) -> None:
        taskName = self._tasksComboBox.currentText()
        if taskName:
            if self._currentTask:
                self._progressBarDialog.show()
                self._progressBarDialog.setValue(0)
                if self._runInBackgroundCheckBox.isChecked():
                    self._taskManager.runTask(task=self._currentTask, background=True)
                else:
                    self._taskManager.runTask(task=self._currentTask, background=False)

    def loadTaskNames(self) -> None:
        self._tasksComboBox.clear()
        self._tasksComboBox.addItem(None)
        for taskName in self._taskManager.taskTypeNames():
            self._tasksComboBox.addItem(taskName)

    def taskProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)

    def taskFinished(self, taskOutput: TaskOutput) -> None:
        LOGGER.info(f'TaskDockWidget.taskFinished() taskOutput={taskOutput}')
        self.signal().finished.emit(taskOutput)
        self._tasksComboBox.setCurrentIndex(0)
        self._progressBarDialog.close()