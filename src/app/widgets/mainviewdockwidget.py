from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.dockwidget import DockWidget
from plugins.pluginmanager import PluginManager

DOCKWIDGETSIZE = (600, 600) # QSettings!


class MainViewDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(MainViewDockWidget, self).__init__(title)
        self._pluginManager = PluginManager()
        self._pluginManager.signal().viewerPluginChanged.connect(self._currentPluginChanged)
        self._initUi()

    def _initUi(self) -> None:
        self._currentPluginChanged(QWidget())

    def _currentPluginChanged(self, plugin):
        if self._pluginManager.isViewerPlugin(plugin):
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignTop)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(plugin)
            widget = QWidget()
            widget.setFixedSize(DOCKWIDGETSIZE[0], DOCKWIDGETSIZE[1])
            widget.setLayout(layout)
            self.setWidget(widget)