from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtWidgets import QSpinBox, QMessageBox, QDoubleSpinBox, QLineEdit

from data.datamanager import DataManager
from plugins.tasks.taskfileselectorwidget import TaskFileSelectorWidget


class TaskSettingsDialog(QDialog):
    def __init__(self, task) -> None:
        super(TaskSettingsDialog, self).__init__()
        self._task = task
        self._formFieldWidgets = {}
        self._dataManager = DataManager()
        self._initUi()

    def _initUi(self) -> None:
        self._formFieldWidgets = self._buildTaskSettingsFormFieldWidgets(self._task)
        buttonsWidget = self._buildButtonsWidget()
        layout = QVBoxLayout()
        for name in self._formFieldWidgets.keys():
            layout.addWidget(self._formFieldWidgets[name][1])   # First label
            layout.addWidget(self._formFieldWidgets[name][0])   # Then form field widget
        layout.addWidget(buttonsWidget)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.resize(self.sizeHint())

    def _buildTaskSettingsFormFieldWidgets(self, task) -> None:
        for name in task.settings().keys():
            setting = task.setting(name)
            if task.checkSettingTypeIsBoolean(setting):
                # Create combobox for boolean values
                comboBox = QComboBox(self)
                comboBox.addItem(None)
                comboBox.addItem('True')
                comboBox.addItem('False')
                self._formFieldWidgets[name] = (comboBox, QLabel(setting.displayName()))            
            elif task.checkSettingTypeIsInteger(setting):
                # Create spinbox for integer values
                spinBox = QSpinBox(self)
                spinBox.setRange(setting.minimum(), setting.maximum())
                self._formFieldWidgets[name] = (spinBox, QLabel(setting.displayName()))            
            elif task.checkSettingTypeIsFloatingPoint(setting):
                # Create spinbox for floating point values
                spinBox = QDoubleSpinBox(self)
                spinBox.setRange(setting.minimum(), setting.maximum())
                self._formFieldWidgets[name] = (spinBox, QLabel(setting.displayName()))            
            elif task.checkSettingTypeIsText(setting):
                # Create line edit
                lineEdit = QLineEdit(self)
                self._formFieldWidgets[name] = (lineEdit, QLabel(setting.displayName()))
            # elif task.checkSettingTypeIsMultiFileSet(setting):
            #     # For this widget we retrieve all multi-filesets
            #     comboBox = QComboBox(self)
            #     comboBox.addItem(None)
            #     multiFileSetModels = self._dataManager.getMultiFileSetModels()
            #     for multiFileSetModel in multiFileSetModels:
            #         comboBox.addItem(multiFileSetModel.name)
            #     comboBox.currentIndexChanged.connect(self._multiFileSetSelected)
            #     self._formFieldWidgets[name] = (comboBox, QLabel(setting.displayName()))            
            # elif task.checkSettingTypeIsFileSet(setting):
            #     # For this widget we need to retrieve all filesets of a given multi-fileset
            #     # but we can only do that after a multi-fileset has been selected
            #     comboBox = QComboBox(self)
            #     comboBox.addItem(None)
            #     comboBox.currentIndexChanged.connect(self._fileSetSelected)
            #     self._formFieldWidgets[name] = (comboBox, QLabel(setting.displayName()))            
            elif task.checkSettingTypeIsFile(setting):
                # for this widget we retrieve all files of a given fileset. This implies
                # that a fileset has been selected
                selectorWidget = TaskFileSelectorWidget(name)
                self._formFieldWidgets[name] = (selectorWidget, QLabel(setting.displayName()))            
            else:
                raise RuntimeError(f'Unknown setting type {name}')
        return self._formFieldWidgets
    
    def _buildButtonsWidget(self) -> None:
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self._cancel)
        saveAndCloseSettingsButton = QPushButton('Save and Close Settings')
        saveAndCloseSettingsButton.clicked.connect(self._saveAndCloseSettings)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addWidget(saveAndCloseSettingsButton)
        buttonsLayout.setAlignment(Qt.AlignRight)
        buttonsWidget = QWidget()
        buttonsWidget.setLayout(buttonsLayout)
        return buttonsWidget
    
    # def _multiFileSetSelected(self, index) -> None:
    #     # What should happen here? Both the fileset and file comboboxes should
    #     # be cleared and repopulated
    #     multiFileSetModelName = self._formFieldWidgets['multiFileSet'][0].currentText()
    #     print(multiFileSetModelName)

    # def _fileSetSelected(self, index) -> None:
    #     pass
    
    def _cancel(self) -> None:
        self.reject()

    def _saveAndCloseSettings(self) -> None:
        # inputDataName = self._inputDataComboBox.currentText()
        # tensorFlowModelFilesName = self._tensorFlowModelFilesComboBox.currentText()
        # if inputDataName and tensorFlowModelFilesName:
        #     self.task().addSetting('inputData', inputDataName)
        #     self.task().addSetting('tensorFlowModelFiles', tensorFlowModelFilesName)
        #     self.accept()
        #     return
        # QMessageBox.critical(self, 'Error', 'Please select input data and TensorFlow model files!')
        pass        

    def show(self):
        return self.exec_()