import os

from PySide6.QtWidgets import QGroupBox, QComboBox, QLabel, QVBoxLayout

from data.datamanager import DataManager


class TaskFileSelectorWidget(QGroupBox):
    def __init__(self) -> None:
        super(TaskFileSelectorWidget, self).__init__()
        self._dataManager = DataManager()
        self._multiFileSetComboBox = None
        self._fileSetComboBox = None
        self._fileComboBox = None
        self._files = {}
        self._groupBox = None
        self._initUi()

    def _initUi(self) -> None:
        # Create comboboxes
        self._multiFileSetComboBox = QComboBox(self)
        self._multiFileSetComboBox.addItem(None)
        registeredMultiFileSetModels = self._dataManager.getRegisteredMultiFileSetModels()
        for registeredMultiFileSetModel in registeredMultiFileSetModels:
            self._multiFileSetComboBox.addItem(registeredMultiFileSetModel.name)
        self._multiFileSetComboBox.currentIndexChanged.connect(self._multiFileSetSelected)
        self._fileSetComboBox = QComboBox(self)
        self._fileSetComboBox.addItem(None)
        self._fileSetComboBox.currentIndexChanged.connect(self._fileSetSelected)
        self._fileComboBox = QComboBox(self)
        self._fileComboBox.addItem(None)
        # Group box
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Multi-File Sets'))
        layout.addWidget(self._multiFileSetComboBox)
        layout.addWidget(QLabel('File Sets'))
        layout.addWidget(self._fileSetComboBox)
        layout.addWidget(QLabel('Files'))
        layout.addWidget(self._fileComboBox)
        self.setLayout(layout)

    def _multiFileSetSelected(self, index) -> None:
        self._fileComboBox.clear()
        self._fileComboBox.addItem(None)
        self._fileSetComboBox.clear()
        self._fileSetComboBox.addItem(None)
        multiFileSetName = self._multiFileSetComboBox.currentText()
        registeredMultiFileSetModel = self._dataManager.getRegisteredMultiFileSetModelByName(name=multiFileSetName)
        for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
            self._fileSetComboBox.addItem(registeredFileSetModel.name)

    def _fileSetSelected(self, index) -> None:
        self._fileComboBox.clear()
        self._files.clear()
        self._fileComboBox.addItem(None)
        fileSetName = self._fileSetComboBox.currentText()
        multiFileSetName = self._multiFileSetComboBox.currentText()
        registeredMultiFileSetModel = self._dataManager.getRegisteredMultiFileSetModelByName(name=multiFileSetName)
        for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
            if registeredFileSetModel.name == fileSetName:
                for registeredFileModel in registeredFileSetModel.registeredFileModels:
                    fileName = os.path.split(registeredFileModel.path)[1]
                    self._fileComboBox.addItem(fileName)
                    self._files[fileName] = registeredFileModel

    def selectedFile(self):
        return self._files[self._fileComboBox.currentText()]
