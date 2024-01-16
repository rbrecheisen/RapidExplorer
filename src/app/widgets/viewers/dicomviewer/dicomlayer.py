from PySide6.QtWidgets import QGraphicsItemGroup
import pydicom
import pydicom.errors

from widgets.viewers.dicomviewer.layer import Layer
from utils import readFromCache, writeToCache


class DicomLayer(Layer):
    def __init__(self) -> None:
        super(DicomLayer, self).__init__(name='dicom')

    def data(self) -> pydicom.FileDataset:
        if self.file():
            content = readFromCache(file=self.file())
            if not content:
                p = pydicom.dcmread(self.file().path())
                p.decompress()
                content = writeToCache(self.file(), fileObject=p)
            p = content.fileObject()
            return p
        
    def createGraphicsItem(self) -> QGraphicsItemGroup:
        pass