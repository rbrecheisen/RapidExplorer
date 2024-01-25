from PySide6.QtWidgets import QGraphicsItemGroup
import pydicom
import pydicom.errors
import numpy as np

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem

from mosamaticdesktop.widgets.viewers.dicomviewer.layer import Layer
from mosamaticdesktop.utils import readFromCache, writeToCache, applyWindowCenterAndWidth


class DicomLayer(Layer):
    def __init__(self) -> None:
        super(DicomLayer, self).__init__(name='dicom', opacity=1.0)
        self._qimage = None
        self._windowLevel = 50
        self._windowWidth = 400

    def data(self) -> pydicom.FileDataset:
        if self.file():
            content = readFromCache(file=self.file())
            if not content:
                data = pydicom.dcmread(self.file().path())
                data.decompress()
                content = writeToCache(file=self.file(), fileObject=data)
            data = content.fileObject()
            return data
        return None
        
    def setWindowLevelAndWidth(self, windowLevel: int, windowWidth: int) -> None:
        self._windowLevel = windowLevel
        self._windowWidth = windowWidth

    def convertDataToQImage(self) -> QImage:
        p = self.data()
        pixelArray = p.pixel_array
        if 'RescaleSlope' in p and 'RescaleIntercept' in p:
            pixelArray = pixelArray * p.RescaleSlope + p.RescaleIntercept
        pixelArray = applyWindowCenterAndWidth(pixelArray, self._windowLevel, self._windowWidth)
        if pixelArray.dtype != np.uint8:
            pixelArray = pixelArray.astype(np.uint8)
        height, width = pixelArray.shape
        bytes_per_line = width
        return QImage(pixelArray.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        group = QGraphicsItemGroup()
        if self.file() and not self._qimage:
            self._qimage = self.convertDataToQImage()
        if self._qimage and self.visible():
            pixmap = QPixmap.fromImage(self._qimage)
            pixmapItem = QGraphicsPixmapItem(pixmap)
            pixmapItem.setOpacity(self.opacity())
            group.addToGroup(pixmapItem)
        return group