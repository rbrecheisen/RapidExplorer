from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox

from plugins.tasks.tasksettingsdialog import TaskSettingsDialog


class L3AutoSegmentationTaskSettingsDialog(TaskSettingsDialog):
    def __init__(self, task) -> None:
        super(L3AutoSegmentationTaskSettingsDialog, self).__init__(task=task)
        self._inputDataComboBox = QComboBox(self)
        self._inputDataComboBox.addItem(None)
        self._inputDataComboBox.addItem('fileset-539853498534')
        self._tensorFlowModelFilesComboBox = QComboBox(self)
        self._tensorFlowModelFilesComboBox.addItem(None)
        self._tensorFlowModelFilesComboBox.addItem('fileset-tfmodel')
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
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Input Data'))
        layout.addWidget(self._inputDataComboBox)
        layout.addWidget(QLabel('TensorFlow Model Files'))
        layout.addWidget(self._tensorFlowModelFilesComboBox)
        layout.addWidget(buttonsWidget)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.resize(self.sizeHint())

    def _cancel(self) -> None:
        self.reject()

    def _saveAndCloseSettings(self) -> None:
        inputDataName = self._inputDataComboBox.currentText()
        tensorFlowModelFilesName = self._tensorFlowModelFilesComboBox.currentText()
        if inputDataName and tensorFlowModelFilesName:
            self.task().addSetting('inputData', inputDataName)
            self.task().addSetting('tensorFlowModelFiles', tensorFlowModelFilesName)
            self.accept()
            return
        QMessageBox.critical(self, 'Error', 'Please select input data and TensorFlow model files!')