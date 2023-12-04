import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QVBoxLayout

from widgets.viewers.viewer import Viewer


class DicomViewer(Viewer):
    NAME = 'DicomViewer'

    def __init__(self) -> None:
        super(DicomViewer, self).__init__()
        self._graphicsView = None
        self._scene = None
        self._dicomImagesSorted = []
        self._dicomAttributeLayersSorted = []
        self._currentImageIndex = 0
        # self._databaseManager = DataManager()
        self._initUi()

    def _initUi(self) -> None:
        self._initGraphicsView()

    def _initGraphicsView(self) -> None:
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        self.setLayout(layout)

    def clearData(self) -> None:
        self._dicomImagesSorted = []
        self._scene.clear()
