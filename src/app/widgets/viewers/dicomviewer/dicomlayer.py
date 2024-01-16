from PySide6.QtWidgets import QGraphicsItemGroup
import pydicom
import pydicom.errors
import numpy as np

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem

from widgets.viewers.dicomviewer.layer import Layer
from utils import readFromCache, writeToCache, applyWindowCenterAndWidth


class DicomLayer(Layer):
    def __init__(self) -> None:
        super(DicomLayer, self).__init__(name='dicom')
        self._qimage = None
        self._windowLevel = 400
        self._windowWidth = 50

    def data(self) -> pydicom.FileDataset:
        if self.file():
            content = readFromCache(file=self.file())
            if not content:
                p = pydicom.dcmread(self.file().path())
                p.decompress()
                content = writeToCache(self.file(), fileObject=p)
            p = content.fileObject()
            return p
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
        if self._qimage:
            pixmap = QPixmap.fromImage(self._image)
            pixmapItem = QGraphicsPixmapItem(pixmap)
            pixmapItem.setOpacity(self.opacity())
            group.addToGroup(pixmapItem)
        return group