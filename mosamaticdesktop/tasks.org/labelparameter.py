from typing import Any

from mosamaticdesktop.tasks.parameter import Parameter


class LabelParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> None:
        super(LabelParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)

    def copy(self):
        return LabelParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
        )