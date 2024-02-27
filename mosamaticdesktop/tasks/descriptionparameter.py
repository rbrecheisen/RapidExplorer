from typing import Any

from mosamaticdesktop.tasks.parameter import Parameter


class DescriptionParameter(Parameter):
    def __init__(self, name: str, description: str) -> None:
        super(DescriptionParameter, self).__init__(name=name, labelText=description, optional=True)

    def copy(self):
        return DescriptionParameter(
            name=self.name(), 
            description=self.labelText()
        )