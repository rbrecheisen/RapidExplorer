import numpy as np

from typing import List

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem

from mosamaticdesktop.widgets.viewers.dicomviewer.layer import Layer
from mosamaticdesktop.utils import convertNumPyArrayToRgbQImage, AlbertaColorMap, readFromCache, writeToCache, tagPixels


class TagLayer(Layer):
    def __init__(self) -> None:
        super(TagLayer, self).__init__(name='tag')
        self._qimage = None
        self._shape = None

    def shape(self) -> List[int]:
        return self._shape

    def setShape(self, shape: List[int]) -> None:
        self._shape = shape

    def data(self) -> np.array:
        if self.file():
            content = readFromCache(file=self.file())
            if not content:
                data = tagPixels(tagFilePath=self.file().path())
                content = writeToCache(file=self.file(), fileObject=data)
            data = content.fileObject()
            data = data.reshape(self.shape())
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