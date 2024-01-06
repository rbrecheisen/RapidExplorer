import inspect

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QProgressDialog

from tasks.task import Task
from tasks.taskwidgetexception import TaskWidgetException
from logger import Logger

LOGGER = Logger()


class TaskWidget(QWidget):    
    # Trick to return the child class name when NAME is retrieved
    # https://chat.openai.com/c/b7bd6334-5ec3-40e3-9af1-93405c68d795
    @classmethod
    def NAME(cls):
        return cls.__qualname__[:-6]
    
    def __init__(self, taskType: Task) -> None:
        super(TaskWidget, self).__init__()
        if not inspect.isclass(taskType):
            raise TaskWidgetException('TaskWidget: argument taskType should be a class')
        self._taskType = taskType
        self._task = None
        self._placeholderWidget = None
        self._progressBarDialog = None
        self._startButton = None
        self._cancelButton = None
        self._test = False
        self.initUi()

    def name(self) -> str:
        return self.__class__.__name__
    
    def setTest(self, test: bool) -> None:
        self._test = test
    
    def initUi(self) -> None:
        self._placeholderWidget = QWidget()
        self._placeholderWidget.setLayout(QVBoxLayout())
        self.initProgressBarDialog()
        self._startButton = QPushButton('Start')
        self._startButton.setObjectName('startButton') # for testing
        self._startButton.clicked.connect(self.startTask)
        self._cancelButton = QPushButton('Cancel')
        self._cancelButton.setObjectName('cancelButton') # for testing
        self._cancelButton.setEnabled(False)
        self._cancelButton.clicked.connect(self.cancelTask)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._startButton)
        buttonLayout.addWidget(self._cancelButton)
        layout = QVBoxLayout()
        layout.addWidget(self._placeholderWidget)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Running task...', 'Abort', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()
    
    # Execution

    def startTask(self) -> None:
        self._task = self._taskType()
        LOGGER.info('TaskWidget: running task...')
        self._task.start()
        self._cancelButton.setEnabled(True)
        if not self._test:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)

    def cancelTask(self) -> None:
        if self._task:
            LOGGER.info('TaskWidget: cancelling task...')
            self._task.setStatusCanceling()
            self._cancelButton.setEnabled(False)
            if not self._test:
                self._progressBarDialog.close()
        else:
            raise TaskWidgetException('TaskWidget: cannot cancel task, start it first')
        
    # Status
        
    def taskIsIdle(self) -> bool:
        if self._task:
            return self._task.statusIsIdle()
        raise TaskWidgetException('TaskWidget: cannot determine task idle status, start it first')
        
    def taskIsStart(self) -> bool:
        if self._task:
            return self._task.statusIsStart()
        raise TaskWidgetException('TaskWidget: cannot determine task start status, start it first')
        
    def taskIsRunning(self) -> bool:
        if self._task:
            return self._task.statusIsRunning()
        raise TaskWidgetException('TaskWidget: cannot determine task running status, start it first')
        
    def taskIsCanceling(self) -> bool:
        if self._task:
            return self._task.statusIsCanceling()
        raise TaskWidgetException('TaskWidget: cannot determine task canceled status, start it first')
        
    def taskIsCanceled(self) -> bool:
        if self._task:
            return self._task.statusIsCanceled()
        raise TaskWidgetException('TaskWidget: cannot determine task canceled status, start it first')
        
    def taskIsFinished(self) -> bool:
        if self._task:
            return self._task.statusIsFinished()
        raise TaskWidgetException('TaskWidget: cannot determine task finished status, start it first')
    
    def taskIsError(self) -> bool:
        if self._task:
            return self._task.statusIsError()
        raise TaskWidgetException('TaskWidget: cannot determine task error status, start it first')