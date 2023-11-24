from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup

from plugins.viewers.layer import Layer


class DicomAttributeLayer(Layer):
    def __init__(self, name: str, index: int, opacity: float=1.0, visible: bool=True) -> None:
        super(DicomAttributeLayer, self).__init__(name, index, opacity, visible)
        self._instanceNumber = -1

    def instanceNumber(self) -> int:
        return self._instanceNumber
    
    def setInstanceNumber(self, instanceNumber: int) -> None:
        self._instanceNumber = instanceNumber

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        textItem = QGraphicsTextItem('Instance number: ' + str(self._instanceNumber))
        textItem.setDefaultTextColor(Qt.white)
        textItem.setPos(10, 10)
        group = QGraphicsItemGroup()
        group.addToGroup(textItem)
        return group