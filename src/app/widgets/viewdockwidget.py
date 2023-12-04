from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog

from widgets.dockwidget import DockWidget
from widgets.viewers.viewermanager import ViewerManager
from widgets.viewersettingsdialog import ViewerSettingsDialog


class ViewsDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(ViewsDockWidget, self).__init__(title)
        self._viewersComboBox = None
        self._viewerManager = ViewerManager()
        self._showSettingsDialogButton = None
        self.initUi()
        self.loadViewers()

    def initUi(self) -> None:
        self._viewersComboBox = QComboBox(self)
        self._viewersComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        self._showSettingsDialogButton = QPushButton('Edit Settings...')
        self._showSettingsDialogButton.setFixedWidth(200)
        self._showSettingsDialogButton.setEnabled(False)
        self._showSettingsDialogButton.clicked.connect(self.showSettingsDialog)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._showSettingsDialogButton)
        buttonLayout.setAlignment(Qt.AlignRight)
        buttonWidget = QWidget()
        buttonWidget.setLayout(buttonLayout)
        layout = QVBoxLayout()
        layout.addWidget(self._viewersComboBox)
        layout.addWidget(buttonWidget)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)

    def currentIndexChanged(self, index):
        viewerName = self._viewersComboBox.itemText(index)
        if viewerName:
            self._showSettingsDialogButton.setEnabled(True)
            self._viewerManager.setCurrentViewerDefinitionName(viewerName)
        else:
            self._showSettingsDialogButton.setEnabled(False)

    def showSettingsDialog(self) -> None:
        viewerDefinitionName = self._viewersComboBox.currentText()
        if viewerDefinitionName:
            settingsDialog = ViewerSettingsDialog(self._viewerManager.viewerSettings(viewerDefinitionName))
            resultCode = settingsDialog.show()
            if resultCode == QDialog.Accepted:
                self._viewerManager.updateViewerSettings(viewerDefinitionName, settingsDialog.viewerSettings())

    def loadViewers(self):
        self._viewersComboBox.clear()
        self._viewersComboBox.addItem(None)
        for viewerDefinitionName in self._viewerManager.viewerDefinitionNames():
            self._viewersComboBox.addItem(viewerDefinitionName)