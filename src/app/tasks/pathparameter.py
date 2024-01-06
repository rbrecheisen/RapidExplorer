from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from tasks.parameter import Parameter


class PathParameter(Parameter):
    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(PathParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        self._pathLineEdit = None
        self.initUi()

    def initUi(self) -> None:
        button = QPushButton('Select Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        self._pathLineEdit = QLineEdit(self)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.labelText()))
        layout.addWidget(self._pathLineEdit)
        layout.addWidget(button)
        self.setLayout(layout)

    def showFileDialog(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Select Path', '.')
        if dirPath:
            self._pathLineEdit.setText(dirPath)
            self.setValue(value=dirPath)
