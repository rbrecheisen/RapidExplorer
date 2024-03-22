import threading

from typing import Dict, List, Any

from PySide6.QtCore import QObject, Signal

from mosamaticdesktop.tasks.parameter import Parameter
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
from mosamaticdesktop.data.datamanager import DataManager
from mosamaticdesktop.logger import Logger
# from mosamaticdesktop.utils import createNameWithTimestamp

LOGGER = Logger()


class Task:
    class TaskSignal(QObject):
        progress = Signal(int)

    @classmethod
    def NAME(cls):
        # Returns class name of child classes
        return cls.__qualname__

    def __init__(self) -> None:
        self._thread = None
        self._parameters = {}
        self._dataManager = DataManager()
        self._signal = Task.TaskSignal()

    def dataManager(self) -> DataManager:
        return self._dataManager

    def signal(self) -> TaskSignal:
        return self._signal

    def start(self) -> None:
        self._thread = threading.Thread(target=self.run)
        self._thread.start()

    def run(self) -> None:
        self.execute()

    def execute(self) -> None:
        raise NotImplementedError()    

    def updateProgress(self, step: int, nrSteps: int) -> None:
        if self._signal:
            self._progress = int(((step + 1) / (nrSteps)) * 100)
            self._signal.progress.emit(self._progress)

    def cancel(self) -> None:
        self._thread.join()

    def parameters(self) -> List[Parameter]:
        return self._parameters.values()

    def parameter(self, name: str) -> Parameter:
        if name in self._parameters.keys():
            return self._parameters[name]
        return None
    
    def parameterValuesAsString(self) -> str:
        string = ''
        for name in self._parameters.keys():
            value = self._parameters[name].value()
            string += f'{name}="{value}", '
        return string[:-2]
    
    def updateParameters(self, parameters: List[Parameter]):
        for parameter in parameters:
            self._parameters[parameter.name()] = parameter
    
    def addDescriptionParameter(self, name: str, description: str) -> Parameter:
        parameter = DescriptionParameter(name=name, description=description)
        self._parameters[parameter.name()] = parameter
        return parameter

    def addLabelParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = LabelParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter

    def addFileSetParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = FileSetParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter
    
    def addMultiFileSetParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = MultiFileSetParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter

    def addPathParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = PathParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter

    def addFilePathParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = FilePathParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter

    def addTextParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = TextParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter

    def addIntegerParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, minimum: int=0, maximum: int=100, step: int=1) -> Parameter:
        parameter = IntegerParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, minimum=minimum, maximum=maximum, step=step)
        LOGGER.info(f'TaskWidget.addIntegerParameter() value={parameter.name()}')
        self._parameters[parameter.name()] = parameter
        return parameter

    def addFloatingPointParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = FloatingPointParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter
    
    def addBooleanParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> Parameter:
        parameter = BooleanParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._parameters[parameter.name()] = parameter
        return parameter

    def addOptionGroupParameter(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, options: List[str]=[]) -> Parameter:
        parameter = OptionGroupParameter(name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, options=options)
        self._parameters[parameter.name()] = parameter
        return parameter
