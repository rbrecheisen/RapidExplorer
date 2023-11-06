from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from rapidx.app.widgets.dockwidget import DockWidget
from rapidx.app.plugins.pluginmanager import PluginManager
from rapidx.plugins.views.dicomfilesetview.dicomfilesetviewplugin import DicomFileSetViewPlugin


class MainViewDockWidget(DockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(MainViewDockWidget, self).__init__(title, parent=parent)
        self._pluginManager = PluginManager()
        self._pluginManager.signal().pluginChanged.connect(self._currentPluginChanged)
        self._pluginLayout = None
        self._pluginLayoutCurrentWidget = QWidget()
        self._pluginContainerWidget = None
        self._viewPlugin = None
        self._initUi()

    def _initUi(self) -> None:
        self._pluginLayout = QVBoxLayout()
        self._pluginLayout.setAlignment(Qt.AlignTop)
        self._pluginLayout.addWidget(self._pluginLayoutCurrentWidget)
        self._pluginContainerWidget = QWidget()
        self._pluginContainerWidget.setLayout(self._pluginLayout)
        self.setWidget(self._pluginContainerWidget)

    def _currentPluginChanged(self, plugin):
        self._pluginLayout.removeWidget(self._pluginLayoutCurrentWidget)
        self._pluginLayoutCurrentWidget = plugin
        self._pluginLayout.addWidget(self._pluginLayoutCurrentWidget)
        self._pluginContainerWidget.setLayout(self._pluginLayout)
        self.setWidget(self._pluginContainerWidget)
