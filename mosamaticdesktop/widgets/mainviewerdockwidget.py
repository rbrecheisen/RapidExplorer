import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar

from mosamaticdesktop.widgets.dockwidget import DockWidget
from mosamaticdesktop.widgets.viewers.dicomviewer.dicomviewer import DicomViewer
from mosamaticdesktop.data.datamanager import DataManager


class MainViewerDockWidget(DockWidget):
    def __init__(self, title: str, progressBar: QProgressBar) -> None:
        super(MainViewerDockWidget, self).__init__(title)
        self._progressBar = progressBar
        self._viewer = None
        self._dataManager = DataManager()
        self.initUi()

    def initUi(self) -> None:
        self._viewer = DicomViewer(progressBar=self._progressBar)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self._viewer)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)