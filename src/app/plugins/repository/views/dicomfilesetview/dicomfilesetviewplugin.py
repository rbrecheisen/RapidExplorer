import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QVBoxLayout

from plugins.viewplugin import ViewPlugin
from data.databasemanager import DatabaseManager
from data.dicomfiletype import DicomFileType
from data.dicomfile import DicomFile
from data.registeredfilesetmodel import RegisteredFileSetModel

WINDOWCENTER = 50
WINDOWWIDTH = 400
PLUGINNAME = 'DICOM Image Series View'


class DicomFileSetViewPlugin(ViewPlugin):
    def __init__(self):
        super(DicomFileSetViewPlugin, self).__init__()
        self._graphicsView = None
        self._scene = None
        self._dicomImages = []
        self._currentImageIndex = 0
        self._databaseManager = DatabaseManager()
        self._initUi()

    def name(self) -> str:
        return PLUGINNAME

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

    def setData(self, data: RegisteredFileSetModel) -> None:
        self._dicomImages = []
        registeredFileSetModel = data
        fileModels = self._databaseManager.getFileSetModelFileModels(registeredFileSetModel)
        x = []
        for fileModel in fileModels:
            if fileModel.fileType == DicomFileType.name:
                dicomFile = self._databaseManager.getFileFromCache(fileModel.id)
                x.append(dicomFile)
            else:
                raise RuntimeError(f'File {fileModel.path} is not a DICOM file')
        x = sorted(x, key=lambda image: image.data().InstanceNumber)
        for item in x:
            self._dicomImages.append(self._convertToQImage(item))
        self._displayDicomImage(self._currentImageIndex)

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
        imageMin = center - width // 2
        imageMax = center + width // 2
        windowedImage = np.clip(image, imageMin, imageMax)
        windowedImage = ((windowedImage - imageMin) / (imageMax - imageMin)) * 255.0
        return windowedImage.astype(np.uint8)
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0 and self._currentImageIndex > 0:
            self._currentImageIndex -= 1
        elif delta < 0 and self._currentImageIndex < len(self._dicomImages) - 1:
            self._currentImageIndex += 1
        self._displayDicomImage(self._currentImageIndex)

    def _displayDicomImage(self, index) -> None:
        image = self._dicomImages[index]
        pixmap = QPixmap.fromImage(image)
        pixmapItem = QGraphicsPixmapItem(pixmap)
        self._scene.clear()
        self._scene.addItem(pixmapItem)
        self._currentImageIndex = index