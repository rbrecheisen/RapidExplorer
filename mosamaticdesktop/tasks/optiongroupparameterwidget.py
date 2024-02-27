from typing import Any, List

from PySide6.QtWidgets import QWidget, QLabel, QComboBox

from mosamaticdesktop.tasks.optiongroupparameter import OptionGroupParameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget


class OptionGroupParameterWidget(ParameterWidget):
    def __init__(self, parameter: OptionGroupParameter, parent: QWidget=None) -> None:
        super(OptionGroupParameterWidget, self).__init__(parameter=parameter, parent=parent)
        self._optionGroupComboBox = None
        self.initUi()

    def initUi(self) -> None:
        self._optionGroupComboBox = QComboBox(self)
        self._optionGroupComboBox.addItem(None)
        for option in self.parameter().options():
            self._optionGroupComboBox.addItem(option)
        if self.parameter().defaultValue() is not None:
            self._optionGroupComboBox.setCurrentText(self.parameter().defaultValue())
            self.parameter().setValue(self.parameter().defaultValue())
        self._optionGroupComboBox.currentTextChanged.connect(self.currentTextChanged)
        self.layout().addWidget(QLabel(self.parameter().labelText()))
        self.layout().addWidget(self._optionGroupComboBox)

    def currentTextChanged(self, text: str) -> None:
        self.parameter().setValue(text)