from typing import Any, List

from mosamaticdesktop.tasks.parameter import Parameter


class MultiFileSetParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> None:
        super(MultiFileSetParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)

    def copy(self):
        return MultiFileSetParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue()
        )