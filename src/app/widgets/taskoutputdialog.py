from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QScrollArea, QMessageBox

from tasks.taskoutput import TaskOutput


class TaskOutputDialog(QDialog):
    def __init__(self, taskOutput: TaskOutput, clipboard: QClipboard) -> None:
        super(TaskOutputDialog, self).__init__()
        self._taskOutput = taskOutput
        self._clipboard = clipboard
        self.initUi()

    def initUi(self) -> None:
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.errorInfoMessageWidget())
        copyTextItemsButton = QPushButton('Copy Text Items', self)
        copyTextItemsButton.clicked.connect(self.copyTextItems)
        layout = QVBoxLayout()
        layout.addWidget(scrollArea)
        layout.addWidget(copyTextItemsButton)
        self.setLayout(layout)

    def errorInfoMessageWidget(self) -> None:
        container = QWidget()
        containerLayout = QVBoxLayout()
        errorInfo = self._taskOutput.errorInfo()
        for item in errorInfo:
            containerLayout.addWidget(QLabel(item))
        container.setLayout(containerLayout)
        return container
    
    def copyTextItems(self) -> None:
        textToCopy = ''
        for item in self._taskOutput.errorInfo():
            textToCopy += item + '\n'
        self._clipboard.setText(textToCopy)
        QMessageBox.information(self, 'Information', 'Errors copied to clipboard!')

    def show(self) -> None:
        self.exec_()