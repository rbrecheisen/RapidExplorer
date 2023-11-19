from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.dockwidget import DockWidget
from plugins.pluginmanager import PluginManager

DOCKWIDGETSIZE = (600, 600)


class MainViewDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(MainViewDockWidget, self).__init__(title)
        self._pluginManager = PluginManager()
        self._pluginManager.signal().pluginChanged.connect(self._currentPluginChanged)
        self._pluginWidget = None
        self._initUi()

    def _initUi(self) -> None:
        self._currentPluginChanged(QWidget())

    def _currentPluginChanged(self, plugin):        
        self._pluginWidget = plugin
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._pluginWidget)
        widget = QWidget()
        widget.setFixedSize(DOCKWIDGETSIZE[0], DOCKWIDGETSIZE[1])
        widget.setLayout(layout)
        self.setWidget(widget)

    # def setData(self, )