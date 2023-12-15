import os
import pydicom
import numpy as np

from typing import List

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QProgressDialog, QSlider
from PySide6.QtWidgets import QVBoxLayout

from widgets.viewers.viewer import Viewer
from widgets.viewers.dicomviewer.dicomattributeslayer import DicomAttributesLayer
from widgets.viewers.dicomviewer.segmentationmasklayer import SegmentationMaskLayer
from data.datamanager import DataManager
from data.fileset import FileSet
from settings.settingfileset import SettingFileSet
from widgets.viewers.dicomviewer.dicomviewerimage import DicomViewerImage
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
        self._dicomViewerImages = []
        self._currentDicomFileSet = None
        self._currentSegmentationFileSet = None
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

    def findSegmentationFileForDicomFile(self, segmentationFileSet: FileSet, dicomFile: DicomFile) -> SegmentationFile:
        dicomFileName = os.path.split(dicomFile.filePath())[1]
        for file in segmentationFileSet.files():
            segmentationFileName = os.path.split(file.path())[1]
            if dicomFileName in segmentationFileName:
                segmentationFile = SegmentationFile(filePath=file.path())
                return segmentationFile
        return None
    
    def findSegmentationFilePathForDicomFilePath(self, segmentationFileSet: FileSet, dicomFilePath: str) -> str:
        dicomFileName = os.path.split(dicomFilePath)[1]
        for file in segmentationFileSet.files():
            segmentationFilePath = file.path()
            segmentationFileName = os.path.split(segmentationFilePath)[1]
            if dicomFileName in segmentationFileName:
                return segmentationFilePath
        return None
    
    def updateSettings(self) -> None:
        newDicomFileSet = False
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        if dicomFileSetName:
            if not self._currentDicomFileSet or (self._currentDicomFileSet and dicomFileSetName != self._currentDicomFileSet.name()):
                self._currentDicomFileSet = self._dataManager.fileSetByName(name=dicomFileSetName)
                newDicomFileSet = True
        newSegmentationFileSet = False
        segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
        if segmentationFileSetName:
            if not self._currentSegmentationFileSet or (self._currentSegmentationFileSet and segmentationFileSetName != self._currentSegmentationFileSet.name()):
                self._currentSegmentationFileSet = self._dataManager.fileSetByName(name=segmentationFileSetName)
                newSegmentationFileSet = True
        if newDicomFileSet:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            nrSteps = self._currentDicomFileSet.nrFiles()
            step = 0
            self._dicomViewerImages = []
            for i in range(len(self._currentDicomFileSet.files())):
                dicomFilePath = self._currentDicomFileSet.files()[i].path()
                dicomViewerImage = DicomViewerImage(dicomFilePath=dicomFilePath, index=i)
                if newSegmentationFileSet:
                    segmentationFilePath = self.findSegmentationFilePathForDicomFilePath(segmentationFileSet=self._currentSegmentationFileSet, dicomFilePath=dicomFilePath)
                    dicomViewerImage.setSegmentationFilePath(segmentationFilePath=segmentationFilePath)
                self._dicomViewerImages.append(dicomViewerImage)
                progress = int((step + 1) / nrSteps * 100)
                self._progressBarDialog.setValue(progress)
                step += 1
            self._dicomViewerImages = sorted(self._dicomViewerImages, key=lambda image: image.dicomFile().data().InstanceNumber)
        self.displayDicomViewerImage(self._currentImageIndex)
                
    # def updateSettings(self) -> None:
    #     dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
    #     if dicomFileSetName:
    #         segmentationFileSet = None
    #         segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
    #         if segmentationFileSetName:
    #             segmentationFileSet = self._dataManager.fileSetByName(name=segmentationFileSetName)
    #         self._progressBarDialog.show()
    #         self._progressBarDialog.setValue(0)
    #         dicomFileSet = self._dataManager.fileSetByName(name=dicomFileSetName)
    #         nrSteps = 2 * dicomFileSet.nrFiles()
    #         step = 0
    #         dicomFiles = []
    #         for i in range(len(dicomFileSet.files())):
    #             item = []
    #             dicomFile = DicomFile(filePath=dicomFileSet.files()[i].path())
    #             item.append(dicomFile)
    #             if segmentationFileSet:
    #                 segmentationFile = self.findSegmentationFileForDicomFile(segmentationFileSet=segmentationFileSet, dicomFile=dicomFile)
    #                 item.append(segmentationFile)
    #             dicomFiles.append(item)
    #             progress = int((step + 1) / nrSteps * 100)
    #             self._progressBarDialog.setValue(progress)
    #             step += 1
    #         dicomFiles = sorted(dicomFiles, key=lambda item: item[0].data().InstanceNumber)
    #         i = 0
    #         for dicomFile in dicomFiles:
    #             self._dicomFilesSorted.append(self.convertToQImage(dicomFile[0]))
    #             if segmentationFileSet:
    #                 self._dicomSegmentationMaskLayersSorted.append(self.createSegmentationMaskLayer(dicomFile[1], i))
    #             attributeLayer = self.createDicomAttributeLayer(dicomFile[0], i)
    #             if segmentationFileSet:
    #                 attributeLayer.setSegmentationFilePath(dicomFile[1].filePath())
    #             self._dicomAttributeLayersSorted.append(attributeLayer)
    #             progress = int((step + 1) / nrSteps * 100)
    #             self._progressBarDialog.setValue(progress)
    #             step += 1
    #             i += 1
    #         self.displayDicomImageAndAttributeLayer(self._currentImageIndex)

    # def convertToQImage(self, dicomFile: DicomFile) -> QImage:
    #     p = dicomFile.data()
    #     pixelArray = p.pixel_array
    #     if 'RescaleSlope' in p and 'RescaleIntercept' in p:
    #         pixelArray = pixelArray * p.RescaleSlope + p.RescaleIntercept
    #     pixelArray = applyWindowCenterAndWidth(pixelArray, self._windowCenter, self._windowWidth)
    #     if pixelArray.dtype != np.uint8:
    #         pixelArray = pixelArray.astype(np.uint8)
    #     height, width = pixelArray.shape
    #     bytes_per_line = width
    #     return QImage(pixelArray.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    # def createDicomAttributeLayer(self, dicomFile: DicomFile, index: int) -> DicomAttributesLayer:
    #     layer = DicomAttributesLayer(name='dicomAttributeLayer', index=index)
    #     layer.setFilePath(dicomFile.filePath())
    #     layer.setInstanceNumber(dicomFile.data().InstanceNumber)
    #     return layer

    # def createSegmentationMaskLayer(self, segmentationFile: SegmentationFile, index: int) -> SegmentationMaskLayer:
    #     layer = SegmentationMaskLayer(name='segmenationMaskLayer', index=index, opacity=0.5)
    #     layer.setFilePath(segmentationFile.filePath())
    #     return layer

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
        elif delta < 0 and self._currentImageIndex < len(self._dicomViewerImages) - 1:
            self._currentImageIndex += 1
        self.displayDicomViewerImage(self._currentImageIndex)

    def displayDicomViewerImage(self, index) -> None:
        if len(self._dicomViewerImages) > 0 and index < len(self._dicomViewerImages):
            dicomViewerImage = self._dicomViewerImages[index]
            self._scene.clear()
            dicomFileLayer = dicomViewerImage.dicomFileLayer()
            self._scene.addItem(dicomFileLayer.createGraphicsItem())
            segmentationMaskLayer = dicomViewerImage.segmentationMaskLayer()
            self._scene.addItem(segmentationMaskLayer.createGraphicsItem())
            dicomAttributesLayer = dicomViewerImage.dicomAttributesLayer()
            self._scene.addItem(dicomAttributesLayer.createGraphicsItem())

    # def displayDicomImageAndAttributeLayer(self, index) -> None:
    #     image = self._dicomFilesSorted[index]
    #     attributeLayer = self._dicomAttributeLayersSorted[index]
    #     segmentationMaskLayer = self._dicomSegmentationMaskLayersSorted[index]
    #     pixmap = QPixmap.fromImage(image)
    #     pixmapItem = QGraphicsPixmapItem(pixmap)
    #     self._scene.clear()
    #     self._scene.addItem(pixmapItem)
    #     # WARNING: do not add layer itself because it will be destroyed on scene.clear()
    #     # Create scene graphics item on-the-fly
    #     self._scene.addItem(segmentationMaskLayer.createGraphicsItem())
    #     self._scene.addItem(attributeLayer.createGraphicsItem())
    #     self._currentImageIndex = index
    
    def clearData(self) -> None:
        self._dicomFilesSorted = []
        self._dicomAttributeLayersSorted = []
        self._scene.clear()
