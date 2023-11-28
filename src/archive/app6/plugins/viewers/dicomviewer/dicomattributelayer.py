from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup

from plugins.viewers.layer import Layer


class DicomAttributeLayer(Layer):
    def __init__(self, name: str, index: int, opacity: float=1.0, visible: bool=True) -> None:
        super(DicomAttributeLayer, self).__init__(name, index, opacity, visible)
        self._fileName = None
        self._instanceNumber = -1

    def setFileName(self, fileName: str) -> None:
        self._fileName = fileName

    def setInstanceNumber(self, instanceNumber: int) -> None:
        self._instanceNumber = instanceNumber

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        group = QGraphicsItemGroup()
        if self._fileName:
            fileNameItem = QGraphicsTextItem('Filename: ' + self._fileName)
            fileNameItem.setDefaultTextColor(Qt.white)
            fileNameItem.setPos(10, 10)
            group.addToGroup(fileNameItem)
        if self._instanceNumber > 0:
            instanceNumberItem = QGraphicsTextItem('Instance number: ' + str(self._instanceNumber))
            instanceNumberItem.setDefaultTextColor(Qt.white)
            instanceNumberItem.setPos(10, 30)
            group.addToGroup(instanceNumberItem)
        return group