from typing import Any

from mosamaticdesktop.tasks.parameter import Parameter


class BooleanParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> None:
        super(BooleanParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)

    def copy(self):
        return BooleanParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(),             
            visible=self.visible(), 
            defaultValue=self.defaultValue()
        )