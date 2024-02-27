import os
import shutil
import threading

from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent #, Signal, QObject
from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QProgressBar, QSlider, QCheckBox, QGridLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtWidgets import QFileDialog

from mosamaticdesktop.widgets.viewers.dicomviewer.dicomlayer import DicomLayer
from mosamaticdesktop.widgets.viewers.dicomviewer.dicominfolayer import DicomInfoLayer
from mosamaticdesktop.widgets.viewers.dicomviewer.segmentationlayer import SegmentationLayer
from mosamaticdesktop.widgets.viewers.dicomviewer.taglayer import TagLayer
from mosamaticdesktop.widgets.viewers.dicomviewer.filesetcombobox import FileSetComboBox
from mosamaticdesktop.utils import isDicomFile
from mosamaticdesktop.data.fileset import FileSet
from mosamaticdesktop.data.datamanager import DataManager
from mosamaticdesktop.data.file import File
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class DicomViewer(QWidget):
    # class ProgressSignal(QObject):
    #     progress = Signal(int)
    class MyGraphicsView(QGraphicsView):
        def __init__(self, parent=None):
            super(DicomViewer.MyGraphicsView, self).__init__(parent)

        def wheelEvent(self, event: QWheelEvent) -> None:
            event.ignore()

    def __init__(self, progressBar: QProgressBar) -> None:
        super(DicomViewer, self).__init__()
        self._progressBar = progressBar
        self._graphicsWidget = None
        self._graphicsView = None
        self._scene = None
        self._layerTuples = []
        self._windowLevel = 50
        self._windowWidth = 400
        # UI
        self._settingsWidget = None
        self._layerTupleSlider = None
        self._segmentationFileOpacityLabel = None
        self._segmentationFileOpacitySlider = None
        self._tagFileOpacityLabel = None
        self._tagFileOpacitySlider = None
        self._dicomFileInfoOpacityLabel = None
        self._dicomFileInfoOpacitySlider = None
        self._inputFileSetComboBox = None
        # Miscellaneous
        self._fullScan = False
        self._fullScanCheckBox = None
        self._currentLayerTupleIndex = 0
        self._exportDirectory = None
        self._dataManager = DataManager()
        self._layout = None
        # self._progressSignal = self.ProgressSignal()
        # self._progressSignal.progress.connect(self.updateProgress)
        self.initUi()

    def initUi(self) -> None:
        self.initGraphicsView()
        self.initSliders()
        self.initFileSetComboBox()
        self._fullScanCheckBox = QCheckBox('Full Scan')
        self._fullScanCheckBox.setCheckState(Qt.Checked if self._fullScan else Qt.Unchecked)
        self._fullScanCheckBox.stateChanged.connect(self.fullScanCheckBoxStateChanged)
        updateViewerButton = QPushButton('Update Viewer')
        updateViewerButton.clicked.connect(self.inputFileSetChanged)
        selectExportDirectoryButton = QPushButton('Select Export Directory')
        selectExportDirectoryButton.clicked.connect(self.selectExportDirectory)
        exportCurrentImageButton = QPushButton('Export Current Image to File')
        exportCurrentImageButton.clicked.connect(self.exportCurrentImage)
        layout = QGridLayout()
        layout.addWidget(self._graphicsView, 0, 0, 1, 2)
        layout.addWidget(QLabel('Image'), 1, 0)
        layout.addWidget(self._layerTupleSlider, 1, 1)
        layout.addWidget(QLabel('Opacity Segmentation'), 2, 0)
        layout.addWidget(self._segmentationFileOpacitySlider, 2, 1)
        layout.addWidget(QLabel('Opacity TAG'), 3, 0)
        layout.addWidget(self._tagFileOpacitySlider, 3, 1)
        layout.addWidget(QLabel('Input File Set'), 4, 0)
        layout.addWidget(self._inputFileSetComboBox, 4, 1)
        layout.addWidget(self._fullScanCheckBox, 5, 1)
        layout.addWidget(updateViewerButton, 6, 1)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(selectExportDirectoryButton)
        buttonLayout.addWidget(exportCurrentImageButton)
        layout.addLayout(buttonLayout, 7, 1)
        self.setLayout(layout)

    def initGraphicsView(self) -> None:
        self._graphicsView = DicomViewer.MyGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText('DICOM Viewer')
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        self._graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def initSliders(self) -> None:
        self._layerTupleSlider = QSlider(Qt.Horizontal, self)
        self._layerTupleSlider.setRange(0, 100)
        self._layerTupleSlider.valueChanged.connect(self.currentLayerTupleIndexChanged)
        self._segmentationFileOpacitySlider = QSlider(Qt.Horizontal, self)
        self._segmentationFileOpacitySlider.setRange(0, 100)
        self._segmentationFileOpacitySlider.setValue(50)
        self._segmentationFileOpacitySlider.valueChanged.connect(self.segmentationFileOpacityChanged)
        self._segmentationFileOpacitySlider.setVisible(False)
        self._tagFileOpacitySlider = QSlider(Qt.Horizontal, self)
        self._tagFileOpacitySlider.setRange(0, 100)
        self._tagFileOpacitySlider.setValue(50)
        self._tagFileOpacitySlider.valueChanged.connect(self.tagFileOpacityChanged)
        self._tagFileOpacitySlider.setVisible(False)

    def initFileSetComboBox(self) -> None:
        self._inputFileSetComboBox = FileSetComboBox(self)

    def findSegmentationFileForDicomFile(self, dicomFile: File, fileSet: FileSet) -> File:
        for file in fileSet.files():
            if file.name() == dicomFile.name() + '.seg.npy':
                return file
        return None

    def findTagFileForDicomFile(self, dicomFile: File, fileSet: FileSet) -> File:
        for file in fileSet.files():
            if file.name() == dicomFile.name() + '.tag':
                return file
            elif file.name() == dicomFile.name()[:-4] + '.tag':
                return file
            else:
                pass
        return None
    
    # def startSetInputFileSet(self, fileSet: FileSet):
    #     worker = threading.Thread(target=self.setInputFileSet, args=(fileSet, ))
    #     worker.start()

    def setInputFileSet(self, fileSet: FileSet) -> None:
        self._segmentationFileOpacitySlider.setVisible(False)
        self._tagFileOpacitySlider.setVisible(False)
        # self._progressBar.setValue(0)
        step = 0
        nrSteps = len(fileSet.files())
        for file in fileSet.files():
            layerTuple = [None, None, None, None] # dicom, numpy, tag, info
            if isDicomFile(filePath=file.path()):
                dicomLayer = DicomLayer()
                dicomLayer.setFile(file=file)
                dicomLayer.setWindowLevelAndWidth(windowLevel=self._windowLevel, windowWidth=self._windowWidth)
                layerTuple[0] = dicomLayer
                segmentationFile = self.findSegmentationFileForDicomFile(dicomFile=file, fileSet=fileSet)
                if segmentationFile:
                    segmentationLayer = SegmentationLayer()
                    segmentationLayer.setFile(file=segmentationFile)
                    layerTuple[1] = segmentationLayer
                    self._segmentationFileOpacitySlider.setVisible(True)
                tagFile = self.findTagFileForDicomFile(dicomFile=file, fileSet=fileSet)
                if tagFile:
                    tagLayer = TagLayer()
                    tagLayer.setFile(file=tagFile)
                    tagLayer.setShape([dicomLayer.data().Rows, dicomLayer.data().Columns])
                    layerTuple[2] = tagLayer
                    self._tagFileOpacitySlider.setVisible(True)
                dicomInfoLayer = DicomInfoLayer()
                dicomInfoLayer.setFile(file=file)
                dicomInfoLayer.setInstanceNumber(instanceNumber=dicomLayer.data().InstanceNumber)
                layerTuple[3] = dicomInfoLayer
                self._layerTuples.append(layerTuple)
            progress = int(((step + 1) / (nrSteps)) * 100)
            # QObject::setParent: Cannot set parent, new parent is in a different thread
            # QObject::startTimer: Timers cannot be started from another thread
            # self._progressSignal.progress.emit(progress)
            step += 1
        if self._fullScan:
            LOGGER.info('Sorting full scan images by instance number...')
            self._layerTuples = sorted(self._layerTuples, key=lambda layerTuple: layerTuple[0].data().InstanceNumber)
        self._layerTupleSlider.setRange(0, len(self._layerTuples) - 1)
        self.displayLayerTuple(self._currentLayerTupleIndex)

    # def updateProgress(self, progress: int) -> None:
    #     self._progressBar.setValue(progress)

    def currentLayerTupleIndexChanged(self, index) -> None:
        if index > 0 and index < len(self._layerTuples):
            self._currentLayerTupleIndex = index
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def segmentationFileOpacityChanged(self, value) -> None:
        if self._layerTuples:
            for layerTuple in self._layerTuples:
                layerTuple[1].setOpacity(value / 100.0)
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def tagFileOpacityChanged(self, value) -> None:
        if self._layerTuples:
            for layerTuple in self._layerTuples:
                layerTuple[2].setOpacity(value / 100.0)
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def fullScanCheckBoxStateChanged(self, state) -> None:
        self._fullScan = True if state == Qt.Checked else False

    def inputFileSetChanged(self) -> None:
        text = self._inputFileSetComboBox.currentText()
        if text:
            self.clearData()
            inputFileSet = self._dataManager.fileSetByName(text)
            # self.startSetInputFileSet(fileSet=inputFileSet)
            self.setInputFileSet(fileSet=inputFileSet)

    def selectExportDirectory(self) -> None:
        self._exportDirectory = QFileDialog.getExistingDirectory(self, 'Select Export Directory')
        LOGGER.info(f'Selected export directory: {self._exportDirectory}')

    def exportCurrentImage(self) -> None:
        if self._currentLayerTupleIndex >= 0 and len(self._layerTuples) > 0:
            if self._exportDirectory:
                file = self._layerTuples[self._currentLayerTupleIndex][0].file()
                if file:
                    fileName = os.path.split(file.path())[1]
                    exportedFilePath = os.path.join(self._exportDirectory, fileName)
                    shutil.copy(file.path(), exportedFilePath)
                    LOGGER.info(f'Exported file {file.path()} to export directory')

    def wheelEvent(self, event) -> None:
        delta = event.angleDelta().y()
        if delta > 0 and self._currentLayerTupleIndex > 0:
            self._currentLayerTupleIndex -= 1
        elif delta < 0 and self._currentLayerTupleIndex < len(self._layerTuples) - 1:
            self._currentLayerTupleIndex += 1
        # Temporarily block slider events
        self._layerTupleSlider.valueChanged.disconnect(self.currentLayerTupleIndexChanged)
        self._layerTupleSlider.setValue(self._currentLayerTupleIndex)
        self._layerTupleSlider.valueChanged.connect(self.currentLayerTupleIndexChanged)
        # Display image
        self.displayLayerTuple(self._currentLayerTupleIndex)

    def displayLayerTuple(self, index: int) -> None:
        if len(self._layerTuples) > 0 and index < len(self._layerTuples):
            layerTuple = self._layerTuples[index]
            self._scene.clear()
            self._scene.addItem(layerTuple[0].createGraphicsItem())
            if layerTuple[1]:
                self._scene.addItem(layerTuple[1].createGraphicsItem())
            if layerTuple[2]:
                self._scene.addItem(layerTuple[2].createGraphicsItem())
            self._scene.addItem(layerTuple[3].createGraphicsItem())

    def clearData(self) -> None:
        self._scene.clear()
        self._layerTuples = []
        item = self._scene.addText('DICOM Viewer')
        item.setDefaultTextColor(Qt.blue)
