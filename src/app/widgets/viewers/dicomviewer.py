import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QVBoxLayout

from widgets.viewers.viewer import Viewer
from data.databasemanager import DatabaseManager
from data.dicomfiletype import DicomFileType
from data.dicomfile import DicomFile
from data.registeredfilesetmodel import RegisteredFileSetModel


class DicomViewer(Viewer):
    def __init__(self) -> None:
        super(DicomViewer, self).__init__(name='DICOM Viewer')
