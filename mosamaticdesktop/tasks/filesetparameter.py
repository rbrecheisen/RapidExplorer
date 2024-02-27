from typing import Any

from mosamaticdesktop.tasks.parameter import Parameter


class FileSetParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None) -> None:
        super(FileSetParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())

    def copy(self):
        return FileSetParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue()
        )