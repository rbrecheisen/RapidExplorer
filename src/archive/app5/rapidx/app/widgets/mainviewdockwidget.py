from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from rapidx.app.widgets.dockwidget import DockWidget
from rapidx.app.plugins.pluginmanager import PluginManager


class MainViewDockWidget(DockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(MainViewDockWidget, self).__init__(title, parent=parent)
        # Dock widget listens to plugin manager's plugin changed signal
        # so when a different plugin is selected in the plugin manager
        # the main view gets updated with this view plugin
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
        if not self._pluginLayoutCurrentWidget:
            self._pluginLayoutCurrentWidget = QWidget()
        self._pluginLayout.addWidget(self._pluginLayoutCurrentWidget)
        self._pluginContainerWidget.setLayout(self._pluginLayout)
        self.setWidget(self._pluginContainerWidget)
