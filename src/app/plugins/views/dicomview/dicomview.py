import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QVBoxLayout

from plugins.view import View
from data.databasemanager import DatabaseManager
from data.dicomfiletype import DicomFileType
from data.dicomfile import DicomFile
from data.registeredfilesetmodel import RegisteredFileSetModel


WINDOWCENTER = 50
WINDOWWIDTH = 400
VIEWNAME = 'DICOM Viewer'


class DicomView(View):
    def __init__(self) -> None:
        super(DicomView, self).__init__()
        self._graphicsView = None
        self._scene = None
        self._sceneLayers = {}
        self._dicomImages = []
        self._currentImageIndex = 0
        self._databaseManager = DatabaseManager()
        self._initUi()

    def _initUi(self) -> None:
        self._initGraphicsView()

    def _initGraphicsView(self) -> None:
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(VIEWNAME)
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        self.setLayout(layout)

    def addData(self, data: RegisteredFileSetModel, name: str) -> None:
        """ 
        If scene layer dictionary already contains this name, replace the dataset
        and refresh the display
        If the dataset is new, create a new layer and add it on top of the last
        one with a default opacity of 1.0 / (Nr. of layers), so if there are two
        layers, the bottom has opacity 1.0. The one on top of it, has opacity 0.5
        When adding layer info to dictionary use the following structure:
        
        self._sceneLayers = {
            'layerName': {
                'index': <index of corresponding base image>,
                'name': <registered file model name>,
                'opacity': 0.5,
                'visible': True/False,
            }
        }

        The index should correspond to the underlying base image the layer corresponds
        to so if the user scrolls to another image, the layer is not visible. You can
        set the layer to invisible by setting 'visible' to False. An index of -1 means
        the layer is always active (but could be invisible).
        """
        pass

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

    def clearData(self) -> None:
        self._dicomImages = []
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