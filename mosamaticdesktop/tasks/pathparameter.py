from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from mosamaticdesktop.tasks.parameter import Parameter


class PathParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(PathParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self._pathLineEdit = None
        self.initUi()

    def initUi(self) -> None:
        button = QPushButton('Select Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        self._pathLineEdit = QLineEdit(self)
        self.layout().addWidget(QLabel(self.labelText()))
        self.layout().addWidget(self._pathLineEdit)
        self.layout().addWidget(button)

    def showFileDialog(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Select Path', '.')
        if dirPath:
            self._pathLineEdit.setText(dirPath)
            self.setValue(value=dirPath)

    def copy(self):
        return PathParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
        )