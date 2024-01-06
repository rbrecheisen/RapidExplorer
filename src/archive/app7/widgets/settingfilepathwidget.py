from PySide6.QtWidgets import QWidget, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from settings.setting import Setting


class TaskSettingFilePathWidget(QWidget):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(TaskSettingFilePathWidget, self).__init__(parent=parent)
        self._setting = setting
        self._filePathLineEdit = QLineEdit(self)
        if self._setting.value():
            self._filePathLineEdit.setTex(self._setting.value())
        button = QPushButton('Select File Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        layout = QVBoxLayout()
        layout.addWidget(self._filePathLineEdit)
        layout.addWidget(button)
        self.setLayout(layout)

    def showFileDialog(self) -> None:
        filePath, _ = QFileDialog.getOpenFileName(self, 'Select File Path', '.')
        if filePath:
            self._filePathLineEdit.setText(filePath)
            self._setting.setValue(value=filePath)
