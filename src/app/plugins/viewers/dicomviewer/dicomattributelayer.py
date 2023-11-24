from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup

from plugins.viewers.layer import Layer


class DicomAttributeLayer(Layer):
    def __init__(self, name: str, index: int, opacity: float=1.0, visible: bool=True) -> None:
        super(DicomAttributeLayer, self).__init__(name, index, opacity, visible)
        self._instanceNumber = -1
        self._patientId = None

    def setInstanceNumber(self, instanceNumber: int) -> None:
        self._instanceNumber = instanceNumber

    def setPatientId(self, patientId: str) -> None:
        self._patientId = patientId

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        group = QGraphicsItemGroup()
        if self._instanceNumber > 0:
            instanceNumberItem = QGraphicsTextItem('Instance number: ' + str(self._instanceNumber))
            instanceNumberItem.setDefaultTextColor(Qt.white)
            instanceNumberItem.setPos(10, 10)   # QSettings!
            group.addToGroup(instanceNumberItem)
        if self._patientId:
            patientIdItem = QGraphicsTextItem('Patient ID: ' + self._patientId)
            patientIdItem.setDefaultTextColor(Qt.white)
            patientIdItem.setPos(10, 30)        # QSettings!
            group.addToGroup(patientIdItem)
        return group