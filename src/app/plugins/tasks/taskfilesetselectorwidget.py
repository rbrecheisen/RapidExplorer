import os

from PySide6.QtWidgets import QGroupBox, QComboBox, QLabel, QVBoxLayout

from data.datamanager import DataManager


class TaskFileSetSelectorWidget(QGroupBox):
    def __init__(self) -> None:
        super(TaskFileSetSelectorWidget, self).__init__()
        self._dataManager = DataManager()
        self._multiFileSetComboBox = None
        self._fileSetComboBox = None
        self._fileSets = {}
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
        # Group box
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Multi-File Sets'))
        layout.addWidget(self._multiFileSetComboBox)
        layout.addWidget(QLabel('File Sets'))
        layout.addWidget(self._fileSetComboBox)
        self.setLayout(layout)

    def _multiFileSetSelected(self, index) -> None:
        self._fileSetComboBox.clear()
        self._fileSets.clear()
        self._fileSetComboBox.addItem(None)
        multiFileSetName = self._multiFileSetComboBox.currentText()
        registeredMultiFileSetModel = self._dataManager.getRegisteredMultiFileSetModelByName(name=multiFileSetName)
        for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
            self._fileSetComboBox.addItem(registeredFileSetModel.name)
            self._fileSets[registeredFileSetModel.name] = registeredFileSetModel

    def selectedFileSet(self):
        return self._fileSets[self._fileSetComboBox.currentText()]