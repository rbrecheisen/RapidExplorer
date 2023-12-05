from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QProgressDialog

from widgets.dockwidget import DockWidget
from widgets.tasksettingsdialog import TaskSettingsDialog
from tasks.taskmanager2 import TaskManager
from tasks.tasksignal import TaskSignal
from data.fileset import FileSet


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._showSettingsDialogButton = None
        self._runSelectedTaskButton = None
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
        self._progressBarDialog = QProgressDialog('Running task...', 'Abort', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def currentIndexChanged(self, index) -> None:
        taskName = self._tasksComboBox.itemText(index)
        if taskName:
            self._showSettingsDialogButton.setEnabled(True)
            task = self._taskManager.task(name=taskName)
            self._taskManager.setCurrentTask(task)
            # self._taskManager.setCurrentTaskDefinitionName(taskName)
        else:
            self._showSettingsDialogButton.setEnabled(False)
            self._runSelectedTaskButton.setEnabled(False)

    def showSettingsDialog(self) -> None:
        taskDefinitionName = self._tasksComboBox.currentText()
        if taskDefinitionName:
            task = self._taskManager.currentTask()
            settingsDialog = TaskSettingsDialog(task.settings())
            resultCode = settingsDialog.show()
            if resultCode == QDialog.Accepted:
                # self._taskManager.updateTaskSettings(taskDefinitionName, settingsDialog.taskSettings())
                self._runSelectedTaskButton.setEnabled(True)
                self._runSelectedTaskButton.setFocus()

    def runSelectedTask(self) -> None:
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._taskManager.runCurrentTask(background=True)

    def loadTaskNames(self) -> None:
        self._tasksComboBox.clear()
        self._tasksComboBox.addItem(None)
        # for taskDefinitionName in self._taskManager.taskDefinitionNames():
        for taskName in self._taskManager.taskNames():
            self._tasksComboBox.addItem(taskName)

    def taskProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)

    def taskFinished(self, outputFileSet: FileSet) -> None:
        self.signal().finished.emit(outputFileSet)
        self._tasksComboBox.setCurrentIndex(0)
        self._progressBarDialog.close()