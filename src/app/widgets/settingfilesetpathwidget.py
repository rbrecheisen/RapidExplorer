from PySide6.QtWidgets import QWidget, QFileDialog, QLineEdit, QVBoxLayout, QPushButton

from settings.setting import Setting


class SettingFileSetPathWidget(QWidget):
    def __init__(self, setting: Setting, parent: QWidget=None) -> None:
        super(SettingFileSetPathWidget, self).__init__(parent=parent)
        self._setting = setting
        self._fileSetPathLineEdit = QLineEdit(self)
        if self._setting.value():
            self._fileSetPathLineEdit.setText(self._setting.value())
        button = QPushButton('Select File Set Path...', self)
        button.setFixedWidth(150)
        button.clicked.connect(self.showFileDialog)
        layout = QVBoxLayout()
        layout.addWidget(self._fileSetPathLineEdit)
        layout.addWidget(button)
        self.setLayout(layout)

    @property
    def textChanged(self):
        return self._fileSetPathLineEdit.textChanged

    def showFileDialog(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Select File Set Path', '.')
        if dirPath:
            self._fileSetPathLineEdit.setText(dirPath)
            self._setting.setValue(dirPath)
