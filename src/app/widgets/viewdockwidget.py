from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from widgets.dockwidget import DockWidget
# from plugins.pluginmanager import PluginManager


class ViewsDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(ViewsDockWidget, self).__init__(title)
        self._viewersComboBox = None
        self.initUi()
        self.loadViewers()

    def initUi(self) -> None:
        self._viewersComboBox = QComboBox(self)
        self._viewersComboBox.currentIndexChanged.connect(self.currentIndexChanged)
        layout = QVBoxLayout()
        layout.addWidget(self._viewersComboBox)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)

    def currentIndexChanged(self, index):
        selectedText = self._viewersComboBox.itemText(index)
        manager = PluginManager()        
        plugin = manager.viewerPlugin(selectedText)
        if plugin:
            manager.setCurrentViewerPlugin(plugin)

    def loadViewers(self):
        pass
        self._comboBoxViewerPlugins.clear()
        self._comboBoxViewerPlugins.addItem(None)
        manager = PluginManager()
        for pluginName in manager.viewerPlugins().keys():
            self._comboBoxViewerPlugins.addItem(pluginName)
