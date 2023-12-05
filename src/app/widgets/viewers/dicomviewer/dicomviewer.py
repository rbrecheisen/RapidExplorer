import os
import pydicom
import numpy as np

from typing import List

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QVBoxLayout

from widgets.viewers.viewer import Viewer
from widgets.viewers.dicomviewer.dicomattributelayer import DicomAttributeLayer
from data.datamanager import DataManager
from settings.settingfileset import SettingFileSet
from widgets.viewers.dicomviewer.dicomfile import DicomFile

SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


class DicomViewer(Viewer):
    NAME = 'DicomViewer'

    def __init__(self) -> None:
        super(DicomViewer, self).__init__()
        self._graphicsView = None
        self._scene = None
        self._dicomFilesSorted = []
        self._dicomAttributeLayersSorted = []
        self._currentImageIndex = 0
        self._qsettings = QSettings(SETTINGSPATH, QSettings.Format.IniFormat)
        self._windowCenter, self._windowWidth = self.windowCenterAndWidth()
        self._dataManager = DataManager()
        self.initSettings()
        self.initUi()

    def initSettings(self) -> None:
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='Images'))
        self.settings().add(SettingFileSet(name='segmentationFileSetName', displayName='Segmentations'))

    def initUi(self) -> None:
        self.initGraphicsView()

    def initGraphicsView(self) -> None:
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        self.setLayout(layout)

    def updateSettings(self) -> None:
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        if dicomFileSetName:
            dicomFileSet = self._dataManager.fileSetByName(name=dicomFileSetName)
            dicomFiles = []
            for file in dicomFileSet.files():
                dicomFile = DicomFile(filePath=file.path())
                dicomFiles.append(dicomFile)
            dicomFiles = sorted(dicomFiles, key=lambda x: x.data().InstanceNumber)
            i = 0
            for dicomFile in dicomFiles:
                self._dicomFilesSorted.append(self.convertToQImage(dicomFile))
                self._dicomAttributeLayersSorted.append(self.createDicomAttributeLayer(dicomFile, i))
                i += 1
            self._displayDicomImageAndAttributeLayer(self._currentImageIndex)

    def convertToQImage(self, dicomFile: DicomFile) -> QImage:
        p = dicomFile.data()
        pixelArray = p.pixel_array
        if 'RescaleSlope' in p and 'RescaleIntercept' in p:
            pixelArray = pixelArray * p.RescaleSlope + p.RescaleIntercept
        pixelArray = self.applyWindowCenterAndWidth(pixelArray, self._windowCenter, self._windowWidth)
        if pixelArray.dtype != np.uint8:
            pixelArray = pixelArray.astype(np.uint8)
        height, width = pixelArray.shape
        bytes_per_line = width
        return QImage(pixelArray.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    def createDicomAttributeLayer(self, dicomFile: DicomFile, index: int) -> DicomAttributeLayer:
        layer = DicomAttributeLayer(name='dicomAttributeLayer', index=index)
        layer.setFileName(dicomFile.filePath())
        layer.setInstanceNumber(dicomFile.data().InstanceNumber)
        return layer

    def applyWindowCenterAndWidth(self, image, center, width) -> np.array:
        imageMin = center - width // 2
        imageMax = center + width // 2
        windowedImage = np.clip(image, imageMin, imageMax)
        windowedImage = ((windowedImage - imageMin) / (imageMax - imageMin)) * 255.0
        return windowedImage.astype(np.uint8)
    
    def windowCenterAndWidth(self) -> List[int]:
        windowCenter = self._qsettings.value('dicomViewerWindowCenter', None)
        if not windowCenter:
            windowCenter = 50
            self._qsettings.setValue('dicomViewerWindowCenter', windowCenter)
        windowWidth = self._qsettings.value('dicomViewerWindowWidth', None)
        if not windowWidth:
            windowWidth = 400
            self._qsettings.setValue('dicomViewerWindowWidth', windowWidth)
        return int(windowCenter), int(windowWidth)

    def wheelEvent(self, event) -> None:
        delta = event.angleDelta().y()
        if delta > 0 and self._currentImageIndex > 0:
            self._currentImageIndex -= 1
        elif delta < 0 and self._currentImageIndex < len(self._dicomFilesSorted) - 1:
            self._currentImageIndex += 1
        self._displayDicomImageAndAttributeLayer(self._currentImageIndex)

    def _displayDicomImageAndAttributeLayer(self, index) -> None:
        image = self._dicomFilesSorted[index]
        attributeLayer = self._dicomAttributeLayersSorted[index]
        pixmap = QPixmap.fromImage(image)
        pixmapItem = QGraphicsPixmapItem(pixmap)
        self._scene.clear()
        self._scene.addItem(pixmapItem)
        # WARNING: do not add layer itself because it will be destroyed on scene.clear()
        self._scene.addItem(attributeLayer.createGraphicsItem())
        self._currentImageIndex = index
    
    def clearData(self) -> None:
        self._dicomFilesSorted = []
        self._scene.clear()
