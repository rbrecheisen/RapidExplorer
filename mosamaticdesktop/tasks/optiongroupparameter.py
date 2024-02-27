from typing import Any, List

from mosamaticdesktop.tasks.parameter import Parameter


class OptionGroupParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, options: List[str]=[]) -> None:
        super(OptionGroupParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue)
        self._options = options

    def options(self) -> List[str]:
        return self._options

    def copy(self):
        return OptionGroupParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
            options=self.options(),
        )