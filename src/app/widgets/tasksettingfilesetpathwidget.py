from PySide6.QtWidgets import QWidget, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from settings.setting import Setting


class TaskSettingFileSetPathWidget(QWidget):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(TaskSettingFileSetPathWidget, self).__init__(parent=parent)
        self._setting = setting
        self._fileSetPathLineEdit = None
        self.initUi()

    def initUi(self) -> None:
        self._fileSetPathLineEdit = QLineEdit(self)
        button = QPushButton('Select File Set Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        layout = QVBoxLayout()
        layout.addWidget(self._fileSetPathLineEdit)
        layout.addWidget(button)
        self.setLayout(layout)

    def showFileDialog(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Select File Set Path', '.')
        if dirPath:
            self._fileSetPathLineEdit.setText(dirPath)
            self._setting.setValue(dirPath)
