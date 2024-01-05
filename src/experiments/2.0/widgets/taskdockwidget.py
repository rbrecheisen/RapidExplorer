from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QProgressDialog, QCheckBox

from widgets.dockwidget import DockWidget
from tasks.taskmanager import TaskManager
from logger import Logger

LOGGER = Logger()


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._tasksComboBox = None
        self._placeHolderWidget = None
        self._taskManager = TaskManager()
        self.initUi()

    def initUi(self) -> None:
        self._tasksComboBox = QComboBox(self)
        self._tasksComboBox.addItems(['Item 1', 'Item 2'])
        self._tasksComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        # self.initProgressBarDialog()
        self._placeHolderWidget = QWidget()
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

    # def currentIndexChanged(self, index) -> None:
    #     taskName = self._tasksComboBox.itemText(index)
    #     if taskName:
    #         self._showSettingsDialogButton.setEnabled(True)
    #         LOGGER.info(f'TaskDockWidget.currentIndexChanged() Creating new task instance: {taskName}')
    #         self._currentTask = self._taskManager.createTaskFromTaskTypeName(name=taskName)
    #     else:
    #         self._showSettingsDialogButton.setEnabled(False)
    #         self._runSelectedTaskButton.setEnabled(False)
    #         self._currentTask = None

    # def showSettingsDialog(self) -> None:
    #     taskName = self._tasksComboBox.currentText()
    #     if taskName:
    #         LOGGER.info(f'TaskDockWidget.showSettingsDialog() currentTask={self._currentTask}')
    #         if not self._currentTask:
    #             LOGGER.info(f'TaskDockWidget.showSettingsDialog() Creating new task instance for: {taskName}')
    #             self._currentTask = self._taskManager.createTaskFromTaskTypeName(name=taskName)
    #         settingsDialog = TaskSettingsDialog(self._currentTask.settings())
    #         resultCode = settingsDialog.show()
    #         if resultCode == QDialog.Accepted:
    #             self._runSelectedTaskButton.setEnabled(True)
    #             self._runSelectedTaskButton.setFocus()

    # def runSelectedTask(self) -> None:
    #     taskName = self._tasksComboBox.currentText()
    #     if taskName:
    #         if self._currentTask:
    #             self._progressBarDialog.show()
    #             self._progressBarDialog.setValue(0)
    #             if self._runInBackgroundCheckBox.isChecked():
    #                 self._taskManager.runTask(task=self._currentTask, background=True)
    #             else:
    #                 self._taskManager.runTask(task=self._currentTask, background=False)

    # def loadTaskNames(self) -> None:
    #     self._tasksComboBox.clear()
    #     self._tasksComboBox.addItem(None)
    #     for taskName in self._taskManager.taskTypeNames():
    #         self._tasksComboBox.addItem(taskName)

    # def taskProgress(self, progress) -> None:
    #     self._progressBarDialog.setValue(progress)

    # def taskFinished(self, taskOutput: TaskOutput) -> None:
    #     LOGGER.info(f'TaskDockWidget.taskFinished() taskOutput={taskOutput}')
    #     self.signal().finished.emit(taskOutput)
    #     self._tasksComboBox.setCurrentIndex(0)
    #     self._progressBarDialog.close()