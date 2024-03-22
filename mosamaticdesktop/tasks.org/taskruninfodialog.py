from typing import List

from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QListWidget, QPushButton, QTabWidget


class TaskRunInfoDialog(QDialog):
    def __init__(self, taskName: str, errors: List[str], warnings: List[str], info: List[str], parent: QWidget=None) -> None:
        super(TaskRunInfoDialog, self).__init__(parent)
        self._taskName = taskName
        self._errors = errors
        self._warnings = warnings
        self._info = info
        self._tabWidget = None
        self._errorListWidget = None
        self._warningsListWidget = None
        self._infoListWidget = None
        self.initUi()
        self.highlightTab()

    def initUi(self) -> None:
        self._errorListWidget = QListWidget(self)
        for error in self._errors:
            self._errorListWidget.addItem(error)
        self._warningsListWidget = QListWidget(self)
        for warning in self._warnings:
            self._warningsListWidget.addItem(warning)
        self._infoListWidget = QListWidget(self)
        for info in self._info:
            self._infoListWidget.addItem(info)
        self._tabWidget = QTabWidget(self)
        self._tabWidget.addTab(self._errorListWidget, 'Errors')
        self._tabWidget.addTab(self._warningsListWidget, 'Warnings')
        self._tabWidget.addTab(self._infoListWidget, 'Info')
        self._tabWidget.setFixedWidth(600)
        closeButton = QPushButton('Close', self)
        closeButton.clicked.connect(self.close)
        layout = QVBoxLayout()
        layout.addWidget(self._tabWidget)
        layout.addWidget(closeButton)
        self.setLayout(layout)
        self.setWindowTitle(f'Run Info for Task {self._taskName}')

    def highlightTab(self) -> None:
        if len(self._errors) > 0:
            self._tabWidget.setCurrentIndex(0)
        elif len(self._warnings) > 0:
            self._tabWidget.setCurrentIndex(1)
        else:
            self._tabWidget.setCurrentIndex(2)

    def show(self):
        return self.exec()
    
    def close(self):
        self.accept()