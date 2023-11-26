import os

from PySide6.QtWidgets import QGroupBox, QComboBox, QLabel, QVBoxLayout

from data.datamanager import DataManager


class TaskMultiFileSetSelectorWidget(QGroupBox):
    def __init__(self) -> None:
        super(TaskMultiFileSetSelectorWidget, self).__init__()
        self._dataManager = DataManager()
        self._multiFileSetComboBox = None
        self._multiFileSets = {}
        self._groupBox = None
        self._initUi()

    def _initUi(self) -> None:
        # Create comboboxes
        self._multiFileSetComboBox = QComboBox(self)
        self._multiFileSetComboBox.addItem(None)
        registeredMultiFileSetModels = self._dataManager.getRegisteredMultiFileSetModels()
        for registeredMultiFileSetModel in registeredMultiFileSetModels:
            self._multiFileSetComboBox.addItem(registeredMultiFileSetModel.name)
            self._multiFileSets[registeredMultiFileSetModel.name] = registeredMultiFileSetModel
        # Group box
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Multi-File Sets'))
        layout.addWidget(self._multiFileSetComboBox)
        self.setLayout(layout)

    def selectedMultiFileSet(self):
        return self._multiFileSets[self._multiFileSetComboBox.currentText()]
