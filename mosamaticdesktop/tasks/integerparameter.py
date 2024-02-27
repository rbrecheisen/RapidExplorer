from typing import Any

from mosamaticdesktop.tasks.parameter import Parameter


class IntegerParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, minimum: int=0, maximum: int=100, step: int=1) -> None:
        super(IntegerParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self._minimum = minimum
        self._maximum = maximum
        self._step = step

    def minimum(self) -> int:
        return self._minimum
    
    def maximum(self) -> int:
        return self._maximum
    
    def step(self) -> int:
        return self._step

    def copy(self):
        return IntegerParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
            minimum=self.minimum(),
            maximum=self.maximum(),
            step=self.step(),
        )