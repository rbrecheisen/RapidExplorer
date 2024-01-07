import inspect

from typing import Any, List

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QLabel, QDialog, QMessageBox
from PySide6.QtWidgets import QSpacerItem, QSizePolicy

from tasks.task import Task
from tasks.taskwidgetexception import TaskWidgetException
from tasks.taskwidgetparameterdialog import TaskWidgetParameterDialog
from tasks.taskprogressmonitor import TaskProgressMonitor
from tasks.parameter import Parameter
from tasks.descriptionparameter import DescriptionParameter
from tasks.labelparameter import LabelParameter
from tasks.filesetparameter import FileSetParameter
from tasks.pathparameter import PathParameter
from tasks.textparameter import TextParameter
from tasks.integerparameter import IntegerParameter
from tasks.floatingpointparameter import FloatingPointParameter
from tasks.booleanparameter import BooleanParameter
from tasks.optiongroupparameter import OptionGroupParameter
from operatingsystem import OperatingSystem
from logger import Logger

LOGGER = Logger()


class TaskWidget(QWidget):    
    # Trick to return the child class name when NAME is retrieved
    # https://chat.openai.com/c/b7bd6334-5ec3-40e3-9af1-93405c68d795
    @classmethod
    def NAME(cls):
        # Returns class name of child classes (and strips of last 6 characters to get the task name itself)
        return cls.__qualname__[:-6]
    
    def __init__(self, taskType: Task) -> None:
        super(TaskWidget, self).__init__()
        if not inspect.isclass(taskType):
            raise TaskWidgetException('TaskWidget: argument taskType should be a class')
        self._taskType = taskType        
        self._task = None
        self._taskParameters = {}
        self._progressBar = None
        self._progressBarLabel = None
        self._startButton = None
        self._cancelButton = None
        self._settingsButton = None
        self._test = False
        self.initUi()

    def name(self) -> str:
        return self.__class__.__name__
    
    def setTest(self, test: bool) -> None:
        self._test = test

    def initUi(self) -> None:
        self._progressBarLabel = QLabel('0 %')
        labelLayout = QHBoxLayout()
        labelLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        labelLayout.addWidget(self._progressBarLabel)
        labelLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self._progressBar = QProgressBar(self)
        self._progressBar.setRange(0, 100)
        self._progressBar.setValue(0)
        self._startButton = QPushButton('Start')
        self._startButton.setObjectName('startButton') # for testing
        self._startButton.clicked.connect(self.startTask)
        self._cancelButton = QPushButton('Cancel')
        self._cancelButton.setObjectName('cancelButton') # for testing
        self._cancelButton.setEnabled(False)
        self._cancelButton.clicked.connect(self.cancelTask)
        self._settingsButton = QPushButton('Set Task Parameters...')
        self._settingsButton.setObjectName('settingsButton') # for testing
        self._settingsButton.clicked.connect(self.showTaskWidgetParameterDialog)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._startButton)
        buttonLayout.addWidget(self._cancelButton)
        buttonLayout.addWidget(self._settingsButton)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        if OperatingSystem.isDarwin():
            layout.addLayout(labelLayout)
        layout.addWidget(self._progressBar)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    # Task parameters
        
    def taskParameter(self, name: str) -> Parameter:
        if name in self._taskParameters.keys():
            return self._taskParameters[name]
        return None
        
    def addDescriptionParameter(self, name: str, description: str) -> Parameter:
        parameter = DescriptionParameter(name=name, description=description)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addLabelParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = LabelParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addFileSetParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = FileSetParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addPathParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = PathParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addTextParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = TextParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addIntegerParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, minimum: int=0, maximum: int=100, step: int=1) -> Parameter:
        parameter = IntegerParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, minimum=minimum, maximum=maximum, step=step)
        LOGGER.info(f'TaskWidget.addIntegerParameter() value={parameter.name()}')
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addFloatingPointParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = FloatingPointParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter
    
    def addBooleanParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = BooleanParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addOptionGroupParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, options: List[str]=[]) -> Parameter:
        parameter = OptionGroupParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, options=options)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    # Task execution

    def startTask(self) -> None:
        self._task = self._taskType() # instantiate class
        LOGGER.info(f'TaskWidget: creating and running task {self._task.name()}...')
        self._task.setParameters(parameters=self._taskParameters)
        self._task.signal().progress.connect(self.taskProgress)
        self._task.signal().finished.connect(self.taskFinished)
        self._task.start()
        self._cancelButton.setEnabled(True)
        self._progressBarLabel.setText('0 %')
        self._progressBar.setValue(0)

    def cancelTask(self) -> None:
        if self._task:
            LOGGER.info('TaskWidget: cancelling task...')
            self._task.cancel()
            self._cancelButton.setEnabled(False)
            self._progressBarLabel.setText('0 %')
            self._progressBar.setValue(0)

    def showTaskWidgetParameterDialog(self) -> None:
        dialog = TaskWidgetParameterDialog(title=self.name(), parameters=self._taskParameters)
        result = dialog.show()
        if result == QDialog.Accepted:
            self._taskParameters = dialog.parameters()
            self.validate()
        
    def taskProgress(self, progress: int) -> None:
        self._progressBarLabel.setText(f'{progress} %')
        self._progressBar.setValue(progress)

    def taskFinished(self, value: bool) -> None:
        self._cancelButton.setEnabled(False)

    # Validation
        
    def validate(self) -> None:
        raise NotImplementedError()
    
    def showValidationError(self, parameterName: str, message: str) -> None:
        QMessageBox.critical(self, f'Validation Error for parameter "{parameterName}"', message)

    # Status (only used for testing)
        
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