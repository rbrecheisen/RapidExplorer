import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout

from rapidx.app.data.db.db import Db
from rapidx.app.data.db.dbgetcommand import DbGetCommand
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.plugins.viewplugin import ViewPlugin

WINDOWCENTER = 400
WINDOWWIDTH = 50


class DicomFileSetViewPlugin(ViewPlugin):
    def __init__(self, parent=None):
        super(DicomFileSetViewPlugin, self).__init__(parent)
        self._graphicsView = None
        self._scene = None
        self._dicomImages = []
        self._initUi()

    def _initUi(self):
        self._initGraphicsView()

    def _initGraphicsView(self):
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        self.setLayout(layout)

    def setFileSetModel(self, fileSetModel: FileSetModel) -> None:
        with Db() as db:
            fileSetModel = DbGetCommand(db, FileSetModel, fileSetModel.unboundId).execute()
            for fileModel in fileSetModel.fileModels:
                cache = FileCache()
                self._dicomImages.append(self._convertToQImage(cache.get(fileModel.id)))
                print(f'Converted file: {fileModel.id}')

    def _convertToQImage(self, dicomFile: DicomFile):
        p = dicomFile.data()
        pixelArray = p.pixel_array
        if 'RescaleSlope' in p and 'RescaleIntercept' in p:
            pixelArray = pixelArray * p.RescaleSlope + p.RescaleIntercept
        pixelArray = self.applyWindowCenterAndWidth(pixelArray, WINDOWCENTER, WINDOWWIDTH)
        if pixelArray.dtype != np.uint8:
            pixelArray = pixelArray.astype(np.uint8)
        height, width = pixelArray.shape
        bytes_per_line = width
        return QImage(pixelArray.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
 
    def applyWindowCenterAndWidth(self, image, center, width):
        imgMin = center - width // 2
        imgMax = center + width // 2
        windowedImg = np.clip(image, imgMin, imgMax)
        windowedImg = ((windowedImg - imgMin) / (imgMax - imgMin)) * 255.0
        return windowedImg.astype(np.uint8)

    def name(self) -> str:
        return 'DICOM Image Series View'