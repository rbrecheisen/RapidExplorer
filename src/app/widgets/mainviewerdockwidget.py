import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from widgets.dockwidget import DockWidget
from widgets.viewers.dicomviewer.dicomviewer import DicomViewer
from data.datamanager import DataManager


class MainViewerDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(MainViewerDockWidget, self).__init__(title)
        self._viewer = None
        self._dataManager = DataManager()
        self.initUi()

    def initUi(self) -> None:
        self._viewer = DicomViewer(self)
        button = QPushButton('Load Example File Set', self)
        button.clicked.connect(self.loadExampleFileSet)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self._viewer)
        layout.addWidget(button)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)

    def loadExampleFileSet(self) -> None:
        fileSet = self._dataManager.fileSetByName(name='pancreasdemo')
        self._viewer.setInputFileSet(fileSet=fileSet)