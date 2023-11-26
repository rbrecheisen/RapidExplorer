from PySide6.QtWidgets import QGroupBox, QComboBox, QLabel, QVBoxLayout

from data.datamanager import DataManager


class TaskFileSelectorWidget(QGroupBox):
    def __init__(self, name: str) -> None:
        super(TaskFileSelectorWidget, self).__init__()
        self._name = name
        self._dataManager = DataManager()
        self._multiFileSetComboBox = None
        self._fileSetComboBox = None
        self._fileComboBox = None
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
        # Use only registered models!!!
        multiFileSetName = self._multiFileSetComboBox.currentText()
        # multiFileSetModel = self._dataManager.getMultiFileSetModelByName(multiFileSetName)
        # fileSetModels = self._dataManager.getFileSetModelsFromMultiFileSetModel(multiFileSetModel)
        # for fileSetModel in fileSetModels:
        #     print(f'FileSetModel: {fileSetModel.id}')

    def _fileSetSelected(self, index) -> None:
        pass

    def selectedMultiFileSetName(self) -> str:
        return self._multiFileSetComboBox.currentText()
    
    def selectedFileSetName(self) -> str:
        return self._fileSetComboBox.currentText()
    
    def selectedFileName(self) -> str:
        return self._fileComboBox.currentText()
