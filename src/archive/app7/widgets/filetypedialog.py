from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox

from data.allfiletype import AllFileType
from data.csvfiletype import CsvFileType
from data.dicomfiletype import DicomFileType
from data.excelfiletype import ExcelFileType
from data.pngfiletype import PngFileType
from data.filetype import FileType


class FileTypeDialog(QDialog):
    def __init__(self, parent: QWidget=None) -> None:
        super(FileTypeDialog, self).__init__(parent)
        self._fileTypes = {}
        self._fileTypeComboBox = None
        self._selectedFileType = None
        self.initUi()
        self.loadFileTypes()

    def initUi(self) -> None:
        self._fileTypeComboBox = QComboBox(self)
        self._recursiveCheckBox.setChecked(False)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('File Types'))
        layout.addWidget(self._fileTypeComboBox)
        layout.addWidget(self.createButtonsWidget())
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setWindowTitle('Select File Type')

    def createButtonsWidget(self) -> QWidget:
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.reject)
        okButton = QPushButton('Ok')
        okButton.setFocus()
        okButton.clicked.connect(self.accept)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addWidget(okButton)
        buttonsLayout.setAlignment(Qt.AlignRight)
        buttonsWidget = QWidget()
        buttonsWidget.setLayout(buttonsLayout)
        return buttonsWidget
    
    def selectedFileType(self) -> FileType:
        fileTypeName = self._fileTypeComboBox.currentText()
        if fileTypeName:
            return self._fileTypes[fileTypeName]
        return None
    
    def loadFileTypes(self) -> None:
        self._fileTypes = {
            AllFileType.NAME: AllFileType,
            CsvFileType.NAME: CsvFileType,
            DicomFileType.NAME: DicomFileType,
            ExcelFileType.NAME: ExcelFileType,
            PngFileType.NAME: PngFileType,
        }
        for fileTypeName in self._fileTypes.keys():
            self._fileTypeComboBox.addItem(fileTypeName)

    def cancel(self) -> None:
        self.reject()

    def ok(self) -> None:
        self.accept()

    def show(self):
        return self.exec_()