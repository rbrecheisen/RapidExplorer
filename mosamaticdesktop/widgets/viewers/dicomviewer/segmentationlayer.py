import numpy as np

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem

from mosamaticdesktop.widgets.viewers.dicomviewer.layer import Layer
from mosamaticdesktop.utils import convertNumPyArrayToRgbQImage, AlbertaColorMap, readFromCache, writeToCache


class SegmentationLayer(Layer):
    def __init__(self) -> None:
        super(SegmentationLayer, self).__init__(name='numpy')
        self._qimage = None

    def data(self) -> np.array:
        if self.file():
            content = readFromCache(file=self.file())
            if not content:
                data = np.load(self.file().path())
                content = writeToCache(file=self.file(), fileObject=data)
            data = content.fileObject()
            return data
        return None

    def convertDataToQImage(self) -> QImage:
        return convertNumPyArrayToRgbQImage(numpyArray=self.data(), colorMap=AlbertaColorMap())

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        group = QGraphicsItemGroup()
        if self.file() and not self._qimage:
            self._qimage = self.convertDataToQImage()
        if self._qimage:
            pixmap = QPixmap.fromImage(self._qimage)
            pixmapItem = QGraphicsPixmapItem(pixmap)
            pixmapItem.setOpacity(self.opacity())
            group.addToGroup(pixmapItem)
        return group