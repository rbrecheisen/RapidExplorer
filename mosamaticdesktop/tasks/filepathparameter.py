from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from mosamaticdesktop.tasks.parameter import Parameter


class FilePathParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(FilePathParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self._pathLineEdit = None
        self.initUi()

    def initUi(self) -> None:
        button = QPushButton('Select File Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        self._pathLineEdit = QLineEdit(self)
        self.layout().addWidget(QLabel(self.labelText()))
        self.layout().addWidget(self._pathLineEdit)
        self.layout().addWidget(button)

    def showFileDialog(self) -> None:
        filePath, _ = QFileDialog.getOpenFileName(self, 'Select File Path', '.')
        if filePath:
            self._pathLineEdit.setText(filePath)
            self.setValue(value=filePath)

    def copy(self):
        return FilePathParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue(),
        )