from typing import Any, List

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QVBoxLayout, QCheckBox

from tasks.parameter import Parameter


class OptionGroupParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, options: List[str]=[], parent: QWidget=None) -> None:
        super(OptionGroupParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        self._options = options
        self._optionGroupComboBox = None
        self.initUi()

    def initUi(self) -> None:
        self._optionGroupComboBox = QCheckBox(self)
        self._optionGroupComboBox.addItem(None)
        for option in self._options:
            self._optionGroupComboBox.addItem(option)
        if self.defaultValue() is not None:
            self._optionGroupComboBox.setCurrentText(self.defaultValue())
        self._optionGroupComboBox.currentTextChanged.connect(self.currentTextChanged)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.labelText()))
        layout.addWidget(self._optionGroupComboBox)
        self.setLayout(layout)

    def currentTextChanged(self, text: str) -> None:
        self.setValue(text)
