import os

from PySide6.QtCore import Qt, QSettings, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.dockwidget import DockWidget
from widgets.viewers.viewer import Viewer
from widgets.viewers.viewermanager import ViewerManager

SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


class MainViewerDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(MainViewerDockWidget, self).__init__(title)
        self._viewerManager = ViewerManager()
        self._viewerManager.signal().currentViewerChanged.connect(self.currentViewerChanged)
        self._settings = QSettings(SETTINGSPATH, QSettings.Format.IniFormat)
        self.initUi()

    def initUi(self) -> None:
        self.currentViewerChanged(QWidget())

    def currentViewerChanged(self, viewer: Viewer):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(viewer)
        widget = QWidget()
        size = self.windowSize()
        widget.setFixedSize(size.width()+10, size.height()+10)
        widget.setLayout(layout)
        self.setWidget(widget)

    def windowSize(self) -> None:
        size = self._settings.value('mainViewerDockWidgetSize', None)
        if not size:
            size = QSize(600, 600)
            self._settings.setValue('mainViewerDockWidgetSize', size)
        return size
