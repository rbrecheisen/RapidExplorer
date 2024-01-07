import os
import inspect

from utils import ParameterLoader
from tasks.parameter import Parameter
from singleton import singleton
from logger import Logger

LOGGER = Logger()


# @singleton
class ParameterCopier:
    # @staticmethod
    # def makeCopy(obj):
    #     init_args = inspect.signature(obj.__class__.__init__).parameters
    #     args_values = {arg: getattr(obj, arg) for arg in init_args if hasattr(obj, arg)}
    #     return obj.__class__(**args_values)
    
    def __init__(self) -> None:
        self._parameterClasses = ParameterLoader.loadParameterClasses(
            parameterDirectoryPath=os.path.dirname(os.path.realpath(__file__)),
            parameterBaseClass=Parameter,
        )
        for className in self._parameterClasses.keys():
            LOGGER.info(f'ParameterCopier: loaded parameter "{className}"')

    def makeCopy(self, obj):
        for cls in self._parameterClasses.values():
            # For some reason, isinstance(obj, cls) doesn't work...
            if obj.__class__.__name__ == cls.__name__:
                LOGGER.info(f'ParameterCopier: copying parameter "{obj.name()}"')
                return obj.copy()