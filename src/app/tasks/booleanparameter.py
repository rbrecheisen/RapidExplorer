from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QVBoxLayout, QCheckBox

from tasks.parameter import Parameter


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
        self._booleanCheckBox.stateChanged.connect(self.stateChanged)
        layout = QVBoxLayout()
        layout.addWidget(self._booleanCheckBox)
        self.setLayout(layout)

    def stateChanged(self, state: int) -> None:
        self.setValue(True if state == Qt.Checked else False)