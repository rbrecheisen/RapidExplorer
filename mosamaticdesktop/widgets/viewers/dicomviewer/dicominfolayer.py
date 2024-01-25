from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup

from mosamaticdesktop.widgets.viewers.dicomviewer.layer import Layer


class DicomInfoLayer(Layer):
    def __init__(self) -> None:
        super(DicomInfoLayer, self).__init__(name='info')
        self._instanceNumber = -1

    def setInstanceNumber(self, instanceNumber: int) -> None:
        self._instanceNumber = instanceNumber

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        y = 10
        group = QGraphicsItemGroup()
        if self.file():
            filePathItem = QGraphicsTextItem(self.file().path())
            filePathItem.setDefaultTextColor(Qt.white)
            filePathItem.setPos(10, y)
            y += 20
            group.addToGroup(filePathItem)
        if self._instanceNumber > -1:
            instanceNumberItem = QGraphicsTextItem(f'Instance Number: {self._instanceNumber}')
            instanceNumberItem.setDefaultTextColor(Qt.white)
            instanceNumberItem.setPos(10, y)
            y += 20
            group.addToGroup(instanceNumberItem)
        return group