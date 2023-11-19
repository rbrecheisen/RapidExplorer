from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

from rapidx.app.plugins.viewplugin import ViewPlugin


class DicomFileViewPlugin(ViewPlugin):
    def __init__(self, parent=None):
        super(DicomFileViewPlugin, self).__init__(parent)
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        self.setLayout(layout)

    def name(self) -> str:
        return 'DICOM Image View'