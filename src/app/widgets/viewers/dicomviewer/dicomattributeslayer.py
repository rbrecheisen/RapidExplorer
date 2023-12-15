from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup

from widgets.viewers.dicomviewer.layer import Layer


class DicomAttributesLayer(Layer):
    def __init__(self, name: str, index: int, opacity: float=1.0, visible: bool=True) -> None:
        super(DicomAttributesLayer, self).__init__(name, index, opacity, visible)
        self._filePath = None
        self._segmentationFilePath = None
        self._instanceNumber = -1

    def setFilePath(self, filePath: str) -> None:
        self._filePath = filePath

    def setSegmentationFilePath(self, filePath: str) -> None:
        self._segmentationFilePath = filePath

    def setInstanceNumber(self, instanceNumber: int) -> None:
        self._instanceNumber = instanceNumber

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        y = 10
        group = QGraphicsItemGroup()
        if self._filePath:
            filePathItem = QGraphicsTextItem('File path: ' + self._filePath)
            filePathItem.setDefaultTextColor(Qt.white)
            filePathItem.setPos(10, y)
            y += 20
            group.addToGroup(filePathItem)
        if self._segmentationFilePath:
            filePathItem = QGraphicsTextItem('Segmentation file path: ' + self._filePath)
            filePathItem.setDefaultTextColor(Qt.white)
            filePathItem.setPos(10, y)
            y += 20
            group.addToGroup(filePathItem)
        if self._instanceNumber > 0:
            instanceNumberItem = QGraphicsTextItem('Instance number: ' + str(self._instanceNumber))
            instanceNumberItem.setDefaultTextColor(Qt.white)
            instanceNumberItem.setPos(10, y)
            y += 20
            group.addToGroup(instanceNumberItem)
        return group