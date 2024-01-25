from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

from mosamaticdesktop.tasks.parameter import Parameter


class TaskWidgetParameterDialog(QDialog):
    def __init__(self, title: str, parameters: Dict[str, Parameter], parent: QWidget=None) -> None:
        super(TaskWidgetParameterDialog, self).__init__(parent)
        self._title = title
        self._parameters = parameters
        self.initUi()

    def parameters(self) -> Dict[str, Parameter]:
        return self._parameters

    def initUi(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        for name in self._parameters.keys():
            layout.addWidget(self._parameters[name])
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
        for parameter in self._parameters.values():
            if not parameter.optional():
                if parameter.value() is None or parameter.value() == '':
                    QMessageBox.critical(self, 'Error', f'Parameter {parameter.name()} cannot be empty!')
                    return
        self.accept()

    # def closeEvent(self, event: QCloseEvent) -> None:
    #     self.hide()
    #     event.ignore()

    def show(self):
        return self.exec_()
