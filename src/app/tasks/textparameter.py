from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QVBoxLayout

from tasks.parameter import Parameter


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
        self._pathLineEdit.textChanged.connect(self.pathChanged)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.labelText()))
        layout.addWidget(self._pathLineEdit)
        self.setLayout(layout)

    def pathChanged(self, text) -> None:
        self.setValue(text)