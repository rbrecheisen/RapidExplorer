import pydicom
import numpy as np

from typing import List

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem

from widgets.viewers.dicomviewer.layer import Layer
from utils import applyWindowCenterAndWidth


class DicomFileLayer(Layer):
    def __init__(self, name: str, index: int, opacity: float=1.0, visible: bool=True) -> None:
        super(DicomFileLayer, self).__init__(name, index, opacity, visible)
        self._filePath = None
        self._windowCenter = 50
        self._windowWidth = 400
        self._image = None

    def setFilePath(self, filePath: str) -> None:
        self._filePath = filePath

    def setWindowCenterAndWidth(self, windowCenterAndWidth: List[int]) -> None:
        self._windowCenter = windowCenterAndWidth[0]
        self._windowWidth = windowCenterAndWidth[1]

    def convertToQImage(self, filePath: str) -> QImage:
        p = pydicom.dcmread(filePath)
        pixelArray = p.pixel_array
        if 'RescaleSlope' in p and 'RescaleIntercept' in p:
            pixelArray = pixelArray * p.RescaleSlope + p.RescaleIntercept
        pixelArray = applyWindowCenterAndWidth(pixelArray, self._windowCenter, self._windowWidth)
        if pixelArray.dtype != np.uint8:
            pixelArray = pixelArray.astype(np.uint8)
        height, width = pixelArray.shape
        bytes_per_line = width
        return QImage(pixelArray.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        group = QGraphicsItemGroup()
        if not self._image and self._filePath:
            self._image = self.convertToQImage(filePath=self._filePath)
        if self._image:
            pixmap = QPixmap.fromImage(self._image)
            pixmapItem = QGraphicsPixmapItem(pixmap)
            pixmapItem.setOpacity(self.opacity())
            group.addToGroup(pixmapItem)
        return group