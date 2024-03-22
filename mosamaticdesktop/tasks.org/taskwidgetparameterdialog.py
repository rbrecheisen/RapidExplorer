from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

from mosamaticdesktop.tasks.parameterwidget import ParameterWidget


class TaskWidgetParameterDialog(QDialog):
    def __init__(self, title: str, parametersWidgets: Dict[str, ParameterWidget], parent: QWidget=None) -> None:
        super(TaskWidgetParameterDialog, self).__init__(parent)
        self._title = title
        self._parametersWidgets = parametersWidgets
        self.initUi()

    def parameterWidgets(self) -> Dict[str, ParameterWidget]:
        return self._parametersWidgets

    def initUi(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        for name in self._parametersWidgets.keys():
            layout.addWidget(self._parametersWidgets[name])
        layout.addWidget(self.createButtonsWidget())
        self.setLayout(layout)
        self.setFixedWidth(500)
        self.setWindowTitle(self._title)

    def createButtonsWidget(self) -> None:
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.cancel)
        saveAndCloseButton = QPushButton('Save and Close')
        saveAndCloseButton.setFocus()
        saveAndCloseButton.clicked.connect(self.saveAndClose)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addWidget(saveAndCloseButton)
        buttonsLayout.setAlignment(Qt.AlignRight)
        buttonsWidget = QWidget()
        buttonsWidget.setLayout(buttonsLayout)
        return buttonsWidget
    
    def cancel(self) -> None:
        self.reject()

    def saveAndClose(self):
        for parameter in self._parametersWidgets.values():
            if not parameter.optional():
                if parameter.value() is None or parameter.value() == '':
                    QMessageBox.critical(self, 'Error', f'Parameter {parameter.name()} cannot be empty!')
                    return
        self.accept()

    def show(self):
        return self.exec_()
