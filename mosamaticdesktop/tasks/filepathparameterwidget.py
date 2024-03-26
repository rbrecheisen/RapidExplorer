from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget
from mosamaticdesktop.utils import Configuration


class FilePathParameterWidget(ParameterWidget):
    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(FilePathParameterWidget, self).__init__(parameter=parameter, parent=parent)
        if self.parameter().defaultValue() is not None:
            self.parameter().setValue(self.parameter().defaultValue())
        self._pathLineEdit = None
        self._settings = Configuration().qSettings()
        self.initUi()

    def initUi(self) -> None:
        button = QPushButton('Select File Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        self._pathLineEdit = QLineEdit(self)
        self.layout().addWidget(QLabel(self.parameter().labelText()))
        self.layout().addWidget(self._pathLineEdit)
        self.layout().addWidget(button)

    def showFileDialog(self) -> None:
        lastFilePath = self._settings.value('lastFileOpened')
        filePath, _ = QFileDialog.getOpenFileName(self, 'Select File Path', lastFilePath)
        if filePath:
            self._pathLineEdit.setText(filePath)
            self.parameter().setValue(value=filePath)
            self._settings.setValue('lastFileOpened', filePath)