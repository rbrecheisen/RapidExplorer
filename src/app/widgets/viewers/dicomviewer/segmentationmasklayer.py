from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup

from widgets.viewers.dicomviewer.layer import Layer


class SegmentationMaskLayer(Layer):
    def __init__(self, name: str, index: int, opacity: float=1.0, visible: bool=True) -> None:
        super(DicomAttributeLayer, self).__init__(name, index, opacity, visible)

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        return super().createGraphicsItem()