from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

from plugins.viewplugin import ViewPlugin

PLUGINNAME = 'DICOM Image View'


class DicomFileViewPlugin(ViewPlugin):
    def __init__(self, parent=None):
        super(DicomFileViewPlugin, self).__init__()
        self._graphicsView = None
        self._scene = None
        self._initUi()

    def name(self) -> str:
        return PLUGINNAME

    def _initUi(self):
        self._initGraphicsView()

    def _initGraphicsView(self):
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        self.setLayout(layout)