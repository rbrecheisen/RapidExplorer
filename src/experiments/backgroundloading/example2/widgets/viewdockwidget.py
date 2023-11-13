from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from widgets.dockwidget import DockWidget
from plugins.pluginmanager import PluginManager


class ViewsDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(ViewsDockWidget, self).__init__(title)
        self._comboBoxViewPlugins = None
        self._initUi()
        self._loadViewPlugins()

    def _initUi(self) -> None:
        self._comboBoxViewPlugins = QComboBox(self)
        self._comboBoxViewPlugins.currentIndexChanged.connect(self._currentIndexChanged)
        layout = QVBoxLayout()
        layout.addWidget(self._comboBoxViewPlugins)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)

    def _currentIndexChanged(self, index):
        selectedText = self._comboBoxViewPlugins.itemText(index)
        manager = PluginManager()        
        plugin = manager.viewPlugin(selectedText)
        if plugin:
            manager.setCurrentPlugin(plugin)

    def _loadViewPlugins(self):
        self._comboBoxViewPlugins.clear()
        self._comboBoxViewPlugins.addItem(None)
        manager = PluginManager()
        for pluginName in manager.viewPlugins().keys():
            self._comboBoxViewPlugins.addItem(pluginName)
