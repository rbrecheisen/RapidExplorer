import os
import inspect

from mosamaticdesktop.utils import ParameterLoader
from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.singleton import singleton
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


@singleton
class ParameterCopier:
    """ This class is needed because when we pass parameters to the TaskWidgetParameterDialog
    they are deleted by the C++ backend after the dialog closes. Re-opening the dialog then
    results in errors. By explicitly making a copy of the parameters BEFORE passing them to
    the dialog, resolves this issue.
    """
    def __init__(self) -> None:
        self._parameterClasses = ParameterLoader.loadParameterClasses(
            parameterDirectoryPath=os.path.dirname(os.path.realpath(__file__)),
            parameterBaseClass=Parameter,
        )

    def makeCopy(self, obj):
        for cls in self._parameterClasses.values():
            # For some reason, isinstance(obj, cls) doesn't work...
            if obj.__class__.__name__ == cls.__name__:
                return obj.copy()