import inspect

from typing import Any, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QProgressBar, QDialog, QMessageBox

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.tasks.taskwidgetexception import TaskWidgetException
from mosamaticdesktop.tasks.taskwidgetparameterdialog import TaskWidgetParameterDialog
from mosamaticdesktop.tasks.taskruninfodialog import TaskRunInfoDialog
from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parametercopier import ParameterCopier
from mosamaticdesktop.tasks.descriptionparameter import DescriptionParameter
from mosamaticdesktop.tasks.labelparameter import LabelParameter
from mosamaticdesktop.tasks.filesetparameter import FileSetParameter
from mosamaticdesktop.tasks.multifilesetparameter import MultiFileSetParameter
from mosamaticdesktop.tasks.pathparameter import PathParameter
from mosamaticdesktop.tasks.filepathparameter import FilePathParameter
from mosamaticdesktop.tasks.textparameter import TextParameter
from mosamaticdesktop.tasks.integerparameter import IntegerParameter
from mosamaticdesktop.tasks.floatingpointparameter import FloatingPointParameter
from mosamaticdesktop.tasks.booleanparameter import BooleanParameter
from mosamaticdesktop.tasks.optiongroupparameter import OptionGroupParameter
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class TaskWidget(QWidget):    
    # Trick to return the child class name when NAME is retrieved
    # https://chat.openai.com/c/b7bd6334-5ec3-40e3-9af1-93405c68d795
    @classmethod
    def NAME(cls):
        # Returns class name of child classes (and strips of last 6 characters to get the task name itself)
        return cls.__qualname__[:-6]
    
    def __init__(self, taskType: Task, progressBar: QProgressBar) -> None:
        super(TaskWidget, self).__init__()
        if not inspect.isclass(taskType):
            raise TaskWidgetException('TaskWidget: argument taskType should be a class')
        self._taskType = taskType        
        self._progressBar = progressBar
        self._task = None
        self._taskParameters = {}
        # We need this class to copy parameters to the TaskWidgetParameterDialog, otherwise the
        # parameters get deleted by C++ after the dialog closes.
        self._taskParameterCopier = ParameterCopier()
        ######
        # self._progressBar = None
        # self._progressBarLabel = None
        self._startButton = None
        self._cancelButton = None
        self._settingsButton = None
        self._runInfoButton = None
        self._test = False
        self.initUi()

    def name(self) -> str:
        return self.__class__.__name__
    
    def setTest(self, test: bool) -> None:
        self._test = test
    
    def initUi(self) -> None:
        # self._progressBarLabel = QLabel('0 %')
        # labelLayout = QHBoxLayout()
        # labelLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # labelLayout.addWidget(self._progressBarLabel)
        # labelLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # self._progressBar = QProgressBar(self)
        # self._progressBar.setRange(0, 100)
        # self._progressBar.setValue(0)
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
        self._runInfoButton = QPushButton('Run Info...')
        self._runInfoButton.setObjectName('runInfoButton')
        self._runInfoButton.setEnabled(False)
        self._runInfoButton.clicked.connect(self.showTaskRunInfoDialog)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._startButton)
        buttonLayout.addWidget(self._cancelButton)
        buttonLayout.addWidget(self._settingsButton)
        buttonLayout.addWidget(self._runInfoButton)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        # if OperatingSystem.isDarwin():
        #     layout.addLayout(labelLayout)
        # layout.addWidget(self._progressBar)
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
    
    def addMultiFileSetParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = MultiFileSetParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addPathParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = PathParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._taskParameters[parameter.name()] = parameter
        return parameter

    def addFilePathParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = FilePathParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
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
        self._task.setParameters(parameters=self._taskParameters)
        self._task.signal().progress.connect(self.taskProgress)
        self._task.signal().finished.connect(self.taskFinished)
        self._task.start()
        self._startButton.setEnabled(False)
        self._cancelButton.setEnabled(True)
        self._runInfoButton.setEnabled(False)
        self._progressBar.setValue(0)

    def cancelTask(self) -> None:
        if self._task:
            self._task.cancel()
            if not self._test:
                self._runInfoButton.setEnabled(True)
                self._cancelButton.setEnabled(False)
                self._startButton.setEnabled(True)
                self._progressBar.setValue(0)

    def showTaskWidgetParameterDialog(self) -> None:
        # Hack: we need to explicitly copy each parameter before passing them to
        # the TaskWidgetParameterDialog. If not, the Qt C++ backend will delete
        # the parameters if we try to show the dialog twice.
        parameters = {}
        for parameter in self._taskParameters.values():
            parameters[parameter.name()] = self._taskParameterCopier.makeCopy(parameter)
        # Show task widget parameter dialog
        dialog = TaskWidgetParameterDialog(title=self.name(), parameters=parameters)
        result = dialog.show()
        if result == QDialog.Accepted:
            self._taskParameters = dialog.parameters()
            self.validate()

    def showTaskRunInfoDialog(self) -> None:
        if self._task:
            dialog = TaskRunInfoDialog(
                taskName=self._task.name(), errors=self._task.errors(), warnings=self._task.warnings(), info=self._task.info())
            dialog.show()
        
    def taskProgress(self, progress: int) -> None:
        if not self._test:
            self._progressBar.setValue(progress)

    def taskFinished(self, value: bool) -> None:
        if not self._test:
            self._runInfoButton.setEnabled(True)
            self._cancelButton.setEnabled(False)
            self._startButton.setEnabled(True)
            if self._task and (self._task.hasErrors() or self._task.hasWarnings()):
                self.showTaskRunInfoDialog()

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