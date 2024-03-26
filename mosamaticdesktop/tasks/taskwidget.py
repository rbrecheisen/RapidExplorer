from typing import Any, List, Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QProgressBar, QDialog, QMessageBox

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget
from mosamaticdesktop.tasks.descriptionparameter import DescriptionParameter
from mosamaticdesktop.tasks.descriptionparameterwidget import DescriptionParameterWidget
from mosamaticdesktop.tasks.labelparameter import LabelParameter
from mosamaticdesktop.tasks.labelparameterwidget import LabelParameterWidget
from mosamaticdesktop.tasks.filesetparameter import FileSetParameter
from mosamaticdesktop.tasks.filesetparameterwidget import FileSetParameterWidget
from mosamaticdesktop.tasks.multifilesetparameter import MultiFileSetParameter
from mosamaticdesktop.tasks.multifilesetparameterwidget import MultiFileSetParameterWidget
from mosamaticdesktop.tasks.pathparameter import PathParameter
from mosamaticdesktop.tasks.pathparameterwidget import PathParameterWidget
from mosamaticdesktop.tasks.filepathparameter import FilePathParameter
from mosamaticdesktop.tasks.filepathparameterwidget import FilePathParameterWidget
from mosamaticdesktop.tasks.textparameter import TextParameter
from mosamaticdesktop.tasks.textparameterwidget import TextParameterWidget
from mosamaticdesktop.tasks.integerparameter import IntegerParameter
from mosamaticdesktop.tasks.integerparameterwidget import IntegerParameterWidget
from mosamaticdesktop.tasks.floatingpointparameter import FloatingPointParameter
from mosamaticdesktop.tasks.floatingpointparameterwidget import FloatingPointParameterWidget
from mosamaticdesktop.tasks.booleanparameter import BooleanParameter
from mosamaticdesktop.tasks.booleanparameterwidget import BooleanParameterWidget
from mosamaticdesktop.tasks.optiongroupparameter import OptionGroupParameter
from mosamaticdesktop.tasks.optiongroupparameterwidget import OptionGroupParameterWidget
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class TaskWidget(QDialog):
    @classmethod
    def NAME(cls):
        # Returns class name of child classes (and strips of last 6 characters to get the task name itself)
        return cls.__qualname__[:-6]

    def __init__(self, taskType: Task) -> None:
        super(TaskWidget, self).__init__()
        self._taskType = taskType
        self._progressBar = QProgressBar(self)
        self._parameterWidgets = self.createTaskParameterWidgetsFromTask(taskType=self._taskType)
        self._task = None
        self._startButton = None
        self._cancelButton = None
        self._closeButton = None
        self.initUi()

    def initUi(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        for parameterName in self._parameterWidgets.keys():
            layout.addWidget(self._parameterWidgets[parameterName])
        layout.addWidget(self._progressBar)
        layout.addWidget(self.createButtonsWidget())
        self.setLayout(layout)
        self.setFixedWidth(500)
        self.setWindowTitle(self.__class__.__name__)

    def createTaskParameterWidgetsFromTask(self, taskType: Task) -> Dict[str, ParameterWidget]:
        widgets = {}
        task = taskType()
        for parameter in task.parameters():
            if isinstance(parameter, DescriptionParameter):
                widgets[parameter.name()] = DescriptionParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, LabelParameter):
                widgets[parameter.name()] = LabelParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, FileSetParameter):
                widgets[parameter.name()] = FileSetParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, MultiFileSetParameter):
                widgets[parameter.name()] = MultiFileSetParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, PathParameter):
                widgets[parameter.name()] = PathParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, FilePathParameter):
                widgets[parameter.name()] = FilePathParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, TextParameter):
                widgets[parameter.name()] = TextParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, IntegerParameter):
                widgets[parameter.name()] = IntegerParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, FloatingPointParameter):
                widgets[parameter.name()] = FloatingPointParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, BooleanParameter):
                widgets[parameter.name()] = BooleanParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, IntegerParameter):
                widgets[parameter.name()] = IntegerParameterWidget(parameter=parameter, parent=self)
            elif isinstance(parameter, OptionGroupParameter):
                widgets[parameter.name()] = OptionGroupParameterWidget(parameter=parameter, parent=self)
        return widgets

    def createButtonsWidget(self) -> None:
        self._startButton = QPushButton('Start')
        self._startButton.setEnabled(True)
        self._startButton.setFocus()
        self._startButton.clicked.connect(self.start)
        self._cancelButton = QPushButton('Cancel')
        self._cancelButton.setEnabled(False)
        self._cancelButton.clicked.connect(self.cancel)
        self._closeButton = QPushButton('Close')
        self._closeButton.setEnabled(True)
        self._closeButton.clicked.connect(self.close)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self._startButton)
        buttonsLayout.addWidget(self._cancelButton)
        buttonsLayout.addWidget(self._closeButton)
        buttonsLayout.setAlignment(Qt.AlignRight)
        buttonsWidget = QWidget()
        buttonsWidget.setLayout(buttonsLayout)
        return buttonsWidget
    
    def validate(self) -> None:
        raise NotImplementedError()
    
    def showValidationError(self, parameterName: str, message: str) -> None:
        QMessageBox.critical(self, f'Validation Error for parameter "{parameterName}"', message)

    def start(self) -> None:
        for parameter in self._parameterWidgets.values():
            if not parameter.optional():
                if parameter.value() is None or parameter.value() == '':
                    QMessageBox.critical(self, 'Error', f'Parameter {parameter.name()} cannot be empty!')
                    return
        self._task = self._taskType()
        self._task.updateParameters(self._parameterWidgets.values())
        self._task.signal().progress.connect(self.progress)
        self._task.start()
        self._startButton.setEnabled(False)
        self._cancelButton.setEnabled(True)
        self._closeButton.setEnabled(False)
        self._progressBar.setValue(0)

    def progress(self, progress: int) -> None:
        self._progressBar.setValue(progress)
        if progress >= 100:
            self._cancelButton.setEnabled(False)
            self._startButton.setEnabled(True)
            self._closeButton.setEnabled(True)            

    def cancel(self) -> None:
        if self._task:
            self._task.cancel()
            self._cancelButton.setEnabled(False)
            self._startButton.setEnabled(True)
            self._closeButton.setEnabled(True)
            self._progressBar.setValue(0)

    def show(self):
        return self.exec_()

    def close(self) -> None:
        self.accept()
