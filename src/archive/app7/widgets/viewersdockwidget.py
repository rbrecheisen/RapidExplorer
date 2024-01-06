from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QDialog

from widgets.dockwidget import DockWidget
from widgets.viewers.viewermanager import ViewerManager
from widgets.viewersettingsdialog import ViewerSettingsDialog


class ViewersDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(ViewersDockWidget, self).__init__(title)
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
        self._updateViewerButton = QPushButton('Update Viewer')
        self._updateViewerButton.setEnabled(False)
        self._updateViewerButton.clicked.connect(self.updateViewer)
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
            self._viewerManager.setCurrentViewer(self._viewerManager.viewer(name=viewerName))
        else:
            self._showSettingsDialogButton.setEnabled(False)

    def showSettingsDialog(self) -> None:
        viewerName = self._viewersComboBox.currentText()
        if viewerName:
            viewer = self._viewerManager.viewer(name=viewerName)
            settingsDialog = ViewerSettingsDialog(viewerSettings=viewer.settings())
            settingsDialog.signal().updated.connect(self.updateViewer)
            resultCode = settingsDialog.show()
            if resultCode == QDialog.Accepted:
                self.updateViewer()
                settingsDialog.signal().updated.disconnect(self.updateViewer)
            else:
                settingsDialog.signal().updated.disconnect(self.updateViewer)

    def updateViewer(self) -> None:
        self._viewerManager.updateViewerSettings()

    def loadViewers(self):
        self._viewersComboBox.clear()
        self._viewersComboBox.addItem(None)
        for viewerName in self._viewerManager.viewerNames():
            self._viewersComboBox.addItem(viewerName)
