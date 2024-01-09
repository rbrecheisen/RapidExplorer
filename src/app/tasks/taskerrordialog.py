from typing import List

from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QListWidget, QPushButton, QTabWidget


class TaskErrorDialog(QDialog):
    def __init__(self, errors: List[str], warnings: List[str], parent: QWidget=None) -> None:
        super(TaskErrorDialog, self).__init__(parent)
        self._errors = errors
        self._warnings = warnings
        self._tabWidget = None
        self._errorListWidget = None
        self._warningsListWidget = None
        self.initUi()

    def initUi(self) -> None:
        self._errorListWidget = QListWidget()
        for error in self._errors:
            self._errorListWidget.addItem(error)
        self._warningsListWidget = QListWidget()
        for warning in self._warnings:
            self._warningsListWidget.addItem(warning)
        self._tabWidget = QTabWidget(self)
        self._tabWidget.addTab(self._errorListWidget, 'Errors')
        self._tabWidget.addTab(self._warningsListWidget, 'Warnings')
        closeButton = QPushButton('Close', self)
        closeButton.clicked.connect(self.close)
        layout = QVBoxLayout()
        layout.addWidget(self._tabWidget)
        layout.addWidget(closeButton)
        self.setLayout(layout)
        self.setWindowTitle('Task Info')

    def show(self):
        return self.exec_()