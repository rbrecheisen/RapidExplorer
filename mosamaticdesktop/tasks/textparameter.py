from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QVBoxLayout

from mosamaticdesktop.tasks.parameter import Parameter


class TextParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(TextParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self._pathLineEdit = None
        self.initUi()

    def initUi(self) -> None:
        self._pathLineEdit = QLineEdit(self)
        self._pathLineEdit.setText(self.defaultValue())
        self._pathLineEdit.textChanged.connect(self.pathChanged)
        self.layout().addWidget(QLabel(self.labelText()))
        self.layout().addWidget(self._pathLineEdit)

    def pathChanged(self, text) -> None:
        self.setValue(text)

    def copy(self):
        return TextParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
        )