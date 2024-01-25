from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QVBoxLayout, QCheckBox

from mosamaticdesktop.tasks.parameter import Parameter


class BooleanParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(BooleanParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        self._booleanCheckBox = None
        self.initUi()

    def initUi(self) -> None:
        self._booleanCheckBox = QCheckBox(self)
        self._booleanCheckBox.setText(self.labelText())
        if self.defaultValue() is not None:
            self._booleanCheckBox.setCheckState(Qt.Checked if self.defaultValue() else Qt.Unchecked)
            self.stateChanged(state=self._booleanCheckBox.checkState())
        self._booleanCheckBox.stateChanged.connect(self.stateChanged)
        self.layout().addWidget(self._booleanCheckBox)

    def stateChanged(self, state: int) -> None:
        self.setValue(True if state == Qt.Checked else False)

    def copy(self):
        return BooleanParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(),             
            visible=self.visible(), 
            defaultValue=self.defaultValue()
        )