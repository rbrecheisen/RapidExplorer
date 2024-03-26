from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget
from mosamaticdesktop.utils import Configuration


class PathParameterWidget(ParameterWidget):
    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(PathParameterWidget, self).__init__(parameter=parameter, parent=parent)
        if self.parameter().defaultValue() is not None:
            self.parameter().setValue(self.parameter().defaultValue())
        self._settings = Configuration().qSettings()
        self._pathLineEdit = None
        self.initUi()

    def initUi(self) -> None:
        button = QPushButton('Select Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        self._pathLineEdit = QLineEdit(self)
        self.layout().addWidget(QLabel(self.parameter().labelText()))
        self.layout().addWidget(self._pathLineEdit)
        self.layout().addWidget(button)

    def showFileDialog(self) -> None:
        lastDirPath = self._settings.value('lastDirectoryOpenend')
        dirPath = QFileDialog.getExistingDirectory(self, 'Select Path', lastDirPath)
        if dirPath:
            self._pathLineEdit.setText(dirPath)
            self.parameter().setValue(value=dirPath)
            self._settings.setValue('lastDirectoryOpened', dirPath)