import os
import json
import pydicom
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QComboBox, QSlider, QCheckBox, QGridLayout, QLabel, QSpacerItem, QSizePolicy

from widgets.viewers.dicomviewer.dicomlayer import DicomLayer
from widgets.viewers.dicomviewer.dicominfolayer import DicomInfoLayer
from widgets.viewers.dicomviewer.numpylayer import NumPyLayer
from widgets.viewers.dicomviewer.taglayer import TagLayer
from widgets.viewers.dicomviewer.filesetcombobox import FileSetComboBox
from utils import isDicomFile
from data.fileset import FileSet
from data.datamanager import DataManager
from data.file import File
from logger import Logger

LOGGER = Logger()


class DicomViewer(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super(DicomViewer, self).__init__(parent)
        self._graphicsWidget = None
        self._graphicsView = None
        self._scene = None
        self._layerTuples = []
        self._windowLevel = 50
        self._windowWidth = 400
        # UI
        self._settingsWidget = None
        self._layerTupleSlider = None
        self._dicomFileOpacityLabel = None
        self._dicomFileOpacitySlider = None
        self._numpyFileOpacityLabel = None
        self._numpyFileOpacitySlider = None
        self._tagFileOpacityLabel = None
        self._tagFileOpacitySlider = None
        self._dicomFileInfoOpacityLabel = None
        self._dicomFileInfoOpacitySlider = None
        self._inputFileSetComboBox = None
        # Miscellaneous
        self._segmentationFile = False
        self._tagFile = False
        self._currentLayerTupleIndex = 0
        self._dataManager = DataManager()
        self._layout = None
        self.initUi()

    def initUi(self) -> None:
        self.initGraphicsView()
        self.initSliders()
        self.initFileSetComboBox()
        layout = QGridLayout()
        # TODO: Hide segmentation and TAG file sliders at first
        layout.addWidget(self._graphicsView, 0, 0, 1, 2)
        layout.addWidget(QLabel('Image'), 1, 0)
        layout.addWidget(self._layerTupleSlider, 1, 1)
        layout.addWidget(QLabel('Opacity DICOM'), 2, 0)
        layout.addWidget(self._dicomFileOpacitySlider, 2, 1)
        layout.addWidget(QLabel('Opacity Segmentation'), 3, 0)
        layout.addWidget(self._numpyFileOpacitySlider, 3, 1)
        layout.addWidget(QLabel('Opacity TAG'), 4, 0)
        layout.addWidget(self._tagFileOpacitySlider, 4, 1)
        layout.addWidget(QLabel('Opacity DICOM Info'), 5, 0)
        layout.addWidget(self._dicomFileInfoOpacitySlider, 5, 1)
        layout.addWidget(QLabel('Input File Set'), 6, 0)
        layout.addWidget(self._inputFileSetComboBox, 6, 1)
        self.setLayout(layout)

    def initGraphicsView(self) -> None:
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText('DICOM Viewer')
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)

    def initSliders(self) -> None:
        # Index        
        self._layerTupleSlider = QSlider(Qt.Horizontal, self)
        self._layerTupleSlider.setRange(0, 100)
        self._layerTupleSlider.valueChanged.connect(self.currentLayerTupleIndexChanged)
        # DicomLayer
        self._dicomFileInfoOpacityLabel = QLabel('Opacity DICOM')
        self._dicomFileOpacitySlider = QSlider(Qt.Horizontal, self)
        self._dicomFileOpacitySlider.setRange(0, 100)
        self._dicomFileOpacitySlider.setValue(100)
        self._dicomFileOpacitySlider.valueChanged.connect(self.dicomFileOpacityChanged)
        # NumPyLayer
        self._numpyFileOpacityLabel = QLabel('Opacity Segmentation')
        self._numpyFileOpacityLabel.setVisible(False)
        self._numpyFileOpacitySlider = QSlider(Qt.Horizontal, self)
        self._numpyFileOpacitySlider.setRange(0, 100)
        self._numpyFileOpacitySlider.setValue(50)
        self._numpyFileOpacitySlider.valueChanged.connect(self.numpyFileOpacityChanged)
        self._numpyFileOpacitySlider.setVisible(False)
        # TagLayer
        self._tagFileOpacityLabel = QLabel('Opacity TAG')
        self._tagFileOpacityLabel.setVisible(False)
        self._tagFileOpacitySlider = QSlider(Qt.Horizontal, self)
        self._tagFileOpacitySlider.setRange(0, 100)
        self._tagFileOpacitySlider.setValue(50)
        self._tagFileOpacitySlider.valueChanged.connect(self.tagFileOpacityChanged)
        self._tagFileOpacitySlider.setVisible(False)
        # DicomInfoLayer
        self._dicomFileInfoOpacityLabel = QLabel('Opacity DICOM Info')
        self._dicomFileInfoOpacitySlider = QSlider(Qt.Horizontal, self)
        self._dicomFileInfoOpacitySlider.setRange(0, 100)
        self._dicomFileInfoOpacitySlider.setValue(100)
        self._dicomFileInfoOpacitySlider.valueChanged.connect(self.dicomFileInfoOpacityChanged)

    def initFileSetComboBox(self) -> None:
        self._inputFileSetComboBox = FileSetComboBox(self)
        self._inputFileSetComboBox.currentTextChanged.connect(self.inputFileSetChanged)

    def findNumPyFileForDicomFile(self, dicomFile: File, fileSet: FileSet) -> File:
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

    def setInputFileSet(self, fileSet: FileSet) -> None:
        # Hide sliders
        self._numpyFileOpacitySlider.setVisible(False)
        self._tagFileOpacitySlider.setVisible(False)
        # Build layers
        for file in fileSet.files():
            layerTuple = [None, None, None, None] # dicom, numpy, tag, info
            if isDicomFile(filePath=file.path()):
                dicomLayer = DicomLayer()
                dicomLayer.setFile(file=file)
                dicomLayer.setWindowLevelAndWidth(windowLevel=self._windowLevel, windowWidth=self._windowWidth)
                layerTuple[0] = dicomLayer
                numpyFile = self.findNumPyFileForDicomFile(dicomFile=file, fileSet=fileSet)
                if numpyFile:
                    numpyLayer = NumPyLayer()
                    numpyLayer.setFile(file=numpyFile)
                    layerTuple[1] = numpyLayer
                    self._numpyFileOpacitySlider.setVisible(True)
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
        # Sort layers
        self._layerTuples = sorted(self._layerTuples, key=lambda layerTuple: layerTuple[0].data().InstanceNumber)
        # Update layer slider range
        self._layerTupleSlider.setRange(0, len(self._layerTuples) - 1)
        # Display first layer
        self.displayLayerTuple(self._currentLayerTupleIndex)

    def currentLayerTupleIndexChanged(self, index) -> None:
        if index > 0 and index < len(self._layerTuples):
            self._currentLayerTupleIndex = index
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def dicomFileOpacityChanged(self, value) -> None:
        if self._layerTuples:
            for layerTuple in self._layerTuples:
                layerTuple[0].setOpacity(value / 100.0)
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def numpyFileOpacityChanged(self, value) -> None:
        if self._layerTuples:
            for layerTuple in self._layerTuples:
                layerTuple[1].setOpacity(value / 100.0)
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def tagFileOpacityChanged(self, value) -> None:
        if self._layerTuples:
            for layerTuple in self._layerTuples:
                layerTuple[2].setOpacity(value / 100.0)
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def dicomFileInfoOpacityChanged(self, value) -> None:
        if self._layerTuples:
            for layerTuple in self._layerTuples:
                layerTuple[3].setOpacity(value / 100.0)
            self.displayLayerTuple(self._currentLayerTupleIndex)

    def inputFileSetChanged(self, text: str) -> None:
        if text:
            inputFileSet = self._dataManager.fileSetByName(text)
            self.setInputFileSet(inputFileSet)

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
        item = self._scene.addText('DICOM Viewer')
        item.setDefaultTextColor(Qt.blue)
