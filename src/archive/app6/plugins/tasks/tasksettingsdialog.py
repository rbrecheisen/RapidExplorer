from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtWidgets import QSpinBox, QMessageBox, QDoubleSpinBox, QLineEdit

from data.datamanager import DataManager
from plugins.tasks.taskfileselectorwidget import TaskFileSelectorWidget
from plugins.tasks.taskfilesetselectorwidget import TaskFileSetSelectorWidget
from plugins.tasks.taskmultifilesetselectorwidget import TaskMultiFileSetSelectorWidget


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
                comboBox = QComboBox(self)
                comboBox.addItem(None)
                comboBox.addItem('True')
                comboBox.addItem('False')
                self._formFieldWidgets[name] = (comboBox, QLabel(self._buildDisplayName(setting)))

            elif task.checkSettingTypeIsInteger(setting):
                spinBox = QSpinBox(self)
                spinBox.setRange(setting.minimum(), setting.maximum())
                self._formFieldWidgets[name] = (spinBox, QLabel(self._buildDisplayName(setting)))            

            elif task.checkSettingTypeIsFloatingPoint(setting):
                spinBox = QDoubleSpinBox(self)
                spinBox.setRange(setting.minimum(), setting.maximum())
                self._formFieldWidgets[name] = (spinBox, QLabel(self._buildDisplayName(setting)))            

            elif task.checkSettingTypeIsText(setting):
                lineEdit = QLineEdit(self)
                self._formFieldWidgets[name] = (lineEdit, QLabel(self._buildDisplayName(setting)))

            elif task.checkSettingTypeIsFileSelector(setting):
                selectorWidget = TaskFileSelectorWidget()
                self._formFieldWidgets[name] = (selectorWidget, QLabel(self._buildDisplayName(setting)))            

            elif task.checkSettingTypeIsFileSetSelector(setting):
                selectorWidget = TaskFileSetSelectorWidget()
                self._formFieldWidgets[name] = (selectorWidget, QLabel(self._buildDisplayName(setting)))

            elif task.checkSettingTypeIsMultiFileSetSelector(setting):
                selectorWidget = TaskMultiFileSetSelectorWidget()
                self._formFieldWidgets[name] = (selectorWidget, QLabel(self._buildDisplayName(setting)))

            else:
                raise RuntimeError(f'Unknown setting type {name}')
        return self._formFieldWidgets
    
    def _buildButtonsWidget(self) -> None:
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self._cancel)
        saveAndCloseSettingsButton = QPushButton('Save and Close Settings')
        saveAndCloseSettingsButton.setFocus()
        saveAndCloseSettingsButton.clicked.connect(self._saveAndCloseSettings)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addWidget(saveAndCloseSettingsButton)
        buttonsLayout.setAlignment(Qt.AlignRight)
        buttonsWidget = QWidget()
        buttonsWidget.setLayout(buttonsLayout)
        return buttonsWidget
    
    def _buildDisplayName(self, setting) -> str:
        displayName = setting.displayName()
        if setting.optional():
            displayName += ' (optional)'
        return displayName
    
    def _cancel(self) -> None:
        self.reject()

    def _saveAndCloseSettings(self) -> None:
        task = self._task
        for name in task.settings().keys():
            setting = task.setting(name)
            if task.checkSettingTypeIsBoolean(setting):
                comboBox = self._formFieldWidgets[name][0]
                setting.setValue(True if comboBox.currentText() == 'True' else False)

            elif task.checkSettingTypeIsInteger(setting):
                spinBox = self._formFieldWidgets[name][0]
                setting.setValue(spinBox.value())

            elif task.checkSettingTypeIsFloatingPoint(setting):
                doubleSpinBox = self._formFieldWidgets[name][0]
                setting.setValue(doubleSpinBox.value())

            elif task.checkSettingTypeIsText(setting):
                lineEdit = self._formFieldWidgets[name][0]
                setting.setValue(lineEdit.text())

            elif task.checkSettingTypeIsFileSelector(setting):
                fileSelector = self._formFieldWidgets[name][0]
                setting.setValue(fileSelector.selectedFile())

            elif task.checkSettingTypeIsFileSetSelector(setting):
                fileSetSelector = self._formFieldWidgets[name][0]
                setting.setValue(fileSetSelector.selectedFileSet())

            elif task.checkSettingTypeIsMultiFileSetSelector(setting):
                multiFileSetSelector = self._formFieldWidgets[name][0]
                setting.setValue(multiFileSetSelector.selectedMultiFileSet())
            else:
                raise RuntimeError(f'Unknown setting type {name}')
        self.accept()

    def show(self):
        return self.exec_()