from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from rapidx.app.widgets.dockwidget import DockWidget
from rapidx.app.plugins.pluginmanager import PluginManager


class ViewsDockWidget(DockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(ViewsDockWidget, self).__init__(title, parent=parent)
        self._comboBoxViews = None
        self._pluginManager = PluginManager()
        self._initUi()
        self._loadViewPlugins()

    def _initUi(self) -> None:
        self._comboBoxViews = QComboBox(self)
        self._comboBoxViews.currentIndexChanged.connect(self._currentIndexChanged)
        layout = QVBoxLayout()
        layout.addWidget(self._comboBoxViews)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)

    def _currentIndexChanged(self, index):
        selectedText = self._comboBoxViews.itemText(index)
        plugin = self._pluginManager.viewPlugin(selectedText)
        if plugin:
            self._pluginManager.setCurrentPlugin(plugin)

    def _loadViewPlugins(self):
        self._comboBoxViews.clear()
        self._comboBoxViews.addItem('')
        for pluginName in self._pluginManager.viewPlugins().keys():
            self._comboBoxViews.addItem(pluginName)
