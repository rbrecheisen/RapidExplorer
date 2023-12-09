import os
import pydicom
import numpy as np

from typing import List

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QProgressDialog, QSlider
from PySide6.QtWidgets import QVBoxLayout

from widgets.viewers.viewer import Viewer
from widgets.viewers.dicomviewer.dicomattributelayer import DicomAttributeLayer
from widgets.viewers.dicomviewer.segmentationmasklayer import SegmentationMaskLayer
from data.datamanager import DataManager
from settings.settingfileset import SettingFileSet
from widgets.viewers.dicomviewer.dicomfile import DicomFile
from widgets.viewers.dicomviewer.segmentationfile import SegmentationFile
from utils import applyWindowCenterAndWidth

SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


class DicomViewer(Viewer):
    NAME = 'DicomViewer'

    def __init__(self) -> None:
        super(DicomViewer, self).__init__()
        self._graphicsView = None
        self._scene = None
        self._imageSlider = None
        self._progressBarDialog = None
        self._dicomFilesSorted = []
        self._dicomAttributeLayersSorted = []
        self._dicomSegmentationMaskLayersSorted = []
        self._currentImageIndex = 0
        self._qsettings = QSettings(SETTINGSPATH, QSettings.Format.IniFormat)
        self._windowCenter, self._windowWidth = self.windowCenterAndWidth()
        self._dataManager = DataManager()
        self.initSettings()
        self.initUi()

    def initSettings(self) -> None:
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='Images'))
        self.settings().add(SettingFileSet(name='segmentationFileSetName', displayName='Segmentations', optional=True))

    def initUi(self) -> None:
        self.initGraphicsView()
        self.initSlider()
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        layout.addWidget(self._imageSlider)
        self.setLayout(layout)
        self.initProgressBarDialog()

    def initGraphicsView(self) -> None:
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)

    def initSlider(self) -> None:
        self._imageSlider = QSlider(Qt.Horizontal, self)
        self._imageSlider.setRange(0, 0)

    def initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Loading Images...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def updateSettings(self) -> None:
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        if dicomFileSetName:
            segmentationFileSet = None
            segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
            if segmentationFileSetName:
                segmentationFileSet = self._dataManager.fileSetByName(name=segmentationFileSetName)
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            dicomFileSet = self._dataManager.fileSetByName(name=dicomFileSetName)
            nrSteps = 2 * dicomFileSet.nrFiles()
            step = 0
            dicomFiles = []
            for i in range(len(dicomFileSet.files())):
                item = []
                dicomFile = DicomFile(filePath=dicomFileSet.files()[i].path())
                item.append(dicomFile)
                if segmentationFileSet:
                    segmentationFile = SegmentationFile(filePath=segmentationFileSet.files()[i].path())
                    item.append(segmentationFile)
                dicomFiles.append(item)
                progress = int((step + 1) / nrSteps * 100)
                self._progressBarDialog.setValue(progress)
                step += 1
            dicomFiles = sorted(dicomFiles, key=lambda item: item[0].data().InstanceNumber)
            i = 0
            for dicomFile in dicomFiles:
                self._dicomFilesSorted.append(self.convertToQImage(dicomFile[0]))
                if segmentationFileSet:
                    self._dicomSegmentationMaskLayersSorted.append(self.createSegmentationMaskLayer(dicomFile[1], i))
                self._dicomAttributeLayersSorted.append(self.createDicomAttributeLayer(dicomFile[0], i))
                progress = int((step + 1) / nrSteps * 100)
                self._progressBarDialog.setValue(progress)
                step += 1
                i += 1
            self._displayDicomImageAndAttributeLayer(self._currentImageIndex)

    def convertToQImage(self, dicomFile: DicomFile) -> QImage:
        p = dicomFile.data()
        pixelArray = p.pixel_array
        if 'RescaleSlope' in p and 'RescaleIntercept' in p:
            pixelArray = pixelArray * p.RescaleSlope + p.RescaleIntercept
        pixelArray = applyWindowCenterAndWidth(pixelArray, self._windowCenter, self._windowWidth)
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

    def createSegmentationMaskLayer(self, segmentationFile: SegmentationFile, index: int) -> SegmentationMaskLayer:
        layer = SegmentationMaskLayer(name='segmenationMaskLayer', index=index)
        return layer

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
        # Create scene graphics item on-the-fly
        self._scene.addItem(attributeLayer.createGraphicsItem())
        self._currentImageIndex = index
    
    def clearData(self) -> None:
        self._dicomFilesSorted = []
        self._dicomAttributeLayersSorted = []
        self._scene.clear()
