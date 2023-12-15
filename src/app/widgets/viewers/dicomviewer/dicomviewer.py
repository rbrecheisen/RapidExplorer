import os

from typing import List

from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QProgressDialog, QSlider
from PySide6.QtWidgets import QVBoxLayout

from widgets.viewers.viewer import Viewer
from data.datamanager import DataManager
from data.fileset import FileSet
from settings.settingfileset import SettingFileSet
from widgets.viewers.dicomviewer.dicomviewerimage import DicomViewerImage
from utils import applyWindowCenterAndWidth

SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


class DicomViewer(Viewer):
    NAME = 'DicomViewer'

    def __init__(self) -> None:
        super(DicomViewer, self).__init__()
        self._graphicsView = None
        self._scene = None
        self._imageSlider = None
        self._segmentationMaskOpacitySlider = None
        self._progressBarDialog = None
        self._dicomViewerImages = []
        self._currentDicomFileSet = None
        self._currentSegmentationFileSet = None
        self._currentImageIndex = 0
        self._settingsQ = QSettings(SETTINGSPATH, QSettings.Format.IniFormat)
        self._windowCenter, self._windowWidth = self.windowCenterAndWidth()
        self._dataManager = DataManager()
        self.initSettings()
        self.initUi()

    def initSettings(self) -> None:
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='Images'))
        self.settings().add(SettingFileSet(name='segmentationFileSetName', displayName='Segmentations', optional=True))

    def initUi(self) -> None:
        self.initGraphicsView()
        self.initSliders()
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        layout.addWidget(self._imageSlider)
        layout.addWidget(self._segmentationMaskOpacitySlider)
        self.setLayout(layout)
        self.initProgressBarDialog()

    def initGraphicsView(self) -> None:
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText(self.name())
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)

    def initSliders(self) -> None:
        self._imageSlider = QSlider(Qt.Horizontal, self)
        self._imageSlider.setRange(0, 100)
        self._imageSlider.valueChanged.connect(self.currentImageIndexChanged)
        self._segmentationMaskOpacitySlider = QSlider(Qt.Horizontal, self)
        self._segmentationMaskOpacitySlider.setRange(0, 100)
        self._segmentationMaskOpacitySlider.setValue(50)
        self._segmentationMaskOpacitySlider.valueChanged.connect(self.segmentationMaskOpacityChanged)

    def initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Loading Images...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

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
                newDicomFileSet = True
        newSegmentationFileSet = False
        segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
        if segmentationFileSetName:
            if not self._currentSegmentationFileSet or (self._currentSegmentationFileSet and segmentationFileSetName != self._currentSegmentationFileSet.name()):
                newSegmentationFileSet = True
        if newDicomFileSet or newSegmentationFileSet:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._currentDicomFileSet = self._dataManager.fileSetByName(name=dicomFileSetName)
            if newSegmentationFileSet:
                self._currentSegmentationFileSet = self._dataManager.fileSetByName(name=segmentationFileSetName)
            nrSteps = self._currentDicomFileSet.nrFiles()
            self._imageSlider.setRange(0, nrSteps-1)
            step = 0
            self._dicomViewerImages = []
            for i in range(len(self._currentDicomFileSet.files())):
                dicomFilePath = self._currentDicomFileSet.files()[i].path()
                dicomViewerImage = DicomViewerImage(dicomFilePath=dicomFilePath, index=i)
                dicomViewerImage.setWindowCenterAndWidth(windowCenterAndWidth=[self._windowCenter, self._windowWidth])
                if newSegmentationFileSet:
                    segmentationFilePath = self.findSegmentationFilePathForDicomFilePath(segmentationFileSet=self._currentSegmentationFileSet, dicomFilePath=dicomFilePath)
                    dicomViewerImage.setSegmentationFilePath(segmentationFilePath=segmentationFilePath)
                self._dicomViewerImages.append(dicomViewerImage)
                progress = int((step + 1) / nrSteps * 100)
                self._progressBarDialog.setValue(progress)
                step += 1
            self._dicomViewerImages = sorted(self._dicomViewerImages, key=lambda image: image.dicomFile().data().InstanceNumber)
        self.displayDicomViewerImage(self._currentImageIndex)
                
    def windowCenterAndWidth(self) -> List[int]:
        windowCenter = self._settingsQ.value('dicomViewerWindowCenter', None)
        if not windowCenter:
            windowCenter = 50
            self._settingsQ.setValue('dicomViewerWindowCenter', windowCenter)
        windowWidth = self._settingsQ.value('dicomViewerWindowWidth', None)
        if not windowWidth:
            windowWidth = 400
            self._settingsQ.setValue('dicomViewerWindowWidth', windowWidth)
        return int(windowCenter), int(windowWidth)

    def wheelEvent(self, event) -> None:
        delta = event.angleDelta().y()
        if delta > 0 and self._currentImageIndex > 0:
            self._currentImageIndex -= 1
        elif delta < 0 and self._currentImageIndex < len(self._dicomViewerImages) - 1:
            self._currentImageIndex += 1
        self._imageSlider.valueChanged.disconnect(self.currentImageIndexChanged)
        self._imageSlider.setValue(self._currentImageIndex)
        self._imageSlider.valueChanged.connect(self.currentImageIndexChanged)
        self.displayDicomViewerImage(self._currentImageIndex)

    def currentImageIndexChanged(self, index: int) -> None:
        if self._currentDicomFileSet:
            if index >= 0 and index < self._currentDicomFileSet.nrFiles():
                self._currentImageIndex = index
                self.displayDicomViewerImage(self._currentImageIndex)

    def segmentationMaskOpacityChanged(self, value: int) -> None:
        for dicomViewerImage in self._dicomViewerImages:
            segmentationMaskLayer = dicomViewerImage.segmentationMaskLayer()
            if segmentationMaskLayer:
                segmentationMaskLayer.setOpacity(value / 100.0)
        self.displayDicomViewerImage(self._currentImageIndex)

    def displayDicomViewerImage(self, index) -> None:
        if len(self._dicomViewerImages) > 0 and index < len(self._dicomViewerImages):
            dicomViewerImage = self._dicomViewerImages[index]
            self._scene.clear()
            self._scene.addItem(dicomViewerImage.dicomFileLayer().createGraphicsItem())
            segmentationMaskLayer = dicomViewerImage.segmentationMaskLayer()
            if segmentationMaskLayer:
                self._scene.addItem(segmentationMaskLayer.createGraphicsItem())
            self._scene.addItem(dicomViewerImage.dicomAttributesLayer().createGraphicsItem())
    
    def clearData(self) -> None:
        self._dicomFilesSorted = []
        self._dicomAttributeLayersSorted = []
        self._scene.clear()
