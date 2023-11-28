import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QVBoxLayout

from plugins.viewers.viewer import Viewer
from plugins.viewers.dicomviewer.dicomattributelayer import DicomAttributeLayer
from data.datamanager import DataManager
from data.dicomfiletype import DicomFileType
from data.dicomfile import DicomFile
from data.registeredfilesetmodel import RegisteredFileSetModel

WINDOWCENTER = 50   # Make this setting!
WINDOWWIDTH = 400


class DicomViewer(Viewer):
    def __init__(self) -> None:
        super(DicomViewer, self).__init__(name='DICOM Viewer')
        self._graphicsView = None
        self._scene = None
        self._dicomImagesSorted = []
        self._dicomAttributeLayersSorted = []
        self._currentImageIndex = 0
        self._databaseManager = DataManager()
        self._initUi()

    def _initUi(self) -> None:
        self._initGraphicsView()

    def _initGraphicsView(self) -> None:
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        self.setLayout(layout)

    def setData(self, data: RegisteredFileSetModel) -> None:
        """ In viewers that inherit from DicomViewer you can allow registered filesets with different file
        types, e.g., the fileset might contain both L3 images and TAG files. 
        """
        self._dicomImagesSorted = []
        self._dicomAttributeLayersSorted = []
        registeredFileSetModel = data
        # fileModels = self._databaseManager.getFileModelsFromRegisteredFileSetModel(registeredFileSetModel)
        fileModels = registeredFileSetModel.registeredFileModels
        dicomImages = []
        for fileModel in fileModels:
            if fileModel.fileType == DicomFileType.name:
                dicomFile = self._databaseManager.getFileFromCache(fileModel.id)
                dicomImages.append(dicomFile)
            else:
                raise RuntimeError(f'File {fileModel.path} is not a DICOM file')
        dicomImages = sorted(dicomImages, key=lambda image: image.data().InstanceNumber)
        i = 0
        for item in dicomImages:
            self._dicomImagesSorted.append(self._convertToQImage(item))
            self._dicomAttributeLayersSorted.append(self._createDicomAttributeLayer(item, i))
            i += 1
        self._displayDicomImageAndAttributeLayer(self._currentImageIndex)

    def clearData(self) -> None:
        self._dicomImagesSorted = []
        self._scene.clear()

    def _convertToQImage(self, dicomFile: DicomFile) -> QImage:
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
    
    def _createDicomAttributeLayer(self, dicomFile: DicomFile, index: int) -> DicomAttributeLayer:
        layer = DicomAttributeLayer(dicomFile.id, index)
        p = dicomFile.data()
        layer.setFileName(dicomFile.name)
        layer.setInstanceNumber(p.InstanceNumber)
        return layer
 
    def applyWindowCenterAndWidth(self, image, center, width) -> np.array:
        imageMin = center - width // 2
        imageMax = center + width // 2
        windowedImage = np.clip(image, imageMin, imageMax)
        windowedImage = ((windowedImage - imageMin) / (imageMax - imageMin)) * 255.0
        return windowedImage.astype(np.uint8)
    
    def wheelEvent(self, event) -> None:
        delta = event.angleDelta().y()
        if delta > 0 and self._currentImageIndex > 0:
            self._currentImageIndex -= 1
        elif delta < 0 and self._currentImageIndex < len(self._dicomImagesSorted) - 1:
            self._currentImageIndex += 1
        self._displayDicomImageAndAttributeLayer(self._currentImageIndex)

    def _displayDicomImageAndAttributeLayer(self, index) -> None:
        image = self._dicomImagesSorted[index]
        attributeLayer = self._dicomAttributeLayersSorted[index]
        pixmap = QPixmap.fromImage(image)
        pixmapItem = QGraphicsPixmapItem(pixmap)
        self._scene.clear()
        self._scene.addItem(pixmapItem)
        # WARNING: do not add layer itself because it will be destroyed on scene.clear()
        self._scene.addItem(attributeLayer.createGraphicsItem())
        self._currentImageIndex = index