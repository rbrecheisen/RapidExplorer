from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from widgets.dockwidget import DockWidget
from plugins.pluginmanager import PluginManager


class ViewsDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(ViewsDockWidget, self).__init__(title)
        self._comboBoxViewerPlugins = None
        self._initUi()
        self._loadViewPlugins()

    def _initUi(self) -> None:
        self._comboBoxViewerPlugins = QComboBox(self)
        self._comboBoxViewerPlugins.currentIndexChanged.connect(self._currentIndexChanged)
        layout = QVBoxLayout()
        layout.addWidget(self._comboBoxViewerPlugins)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)

    def _currentIndexChanged(self, index):
        selectedText = self._comboBoxViewerPlugins.itemText(index)
        manager = PluginManager()        
        plugin = manager.viewerPlugin(selectedText)
        if plugin:
            manager.setCurrentViewerPlugin(plugin)

    def _loadViewPlugins(self):
        self._comboBoxViewerPlugins.clear()
        self._comboBoxViewerPlugins.addItem(None)
        manager = PluginManager()
        for pluginName in manager.viewerPlugins().keys():
            self._comboBoxViewerPlugins.addItem(pluginName)
