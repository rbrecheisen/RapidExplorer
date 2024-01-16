import os
import json
import pydicom
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QComboBox, QSlider

from utils import isDicomFile, isNumPyFile, isTagFile, tagPixels, readFromCache, writeToCache
from data.fileset import FileSet
from data.file import File
from logger import Logger

LOGGER = Logger()


class DicomViewer(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super(DicomViewer, self).__init__(parent)
        self._graphicsView = None
        self._scene = None
        self._fileTuples = []
        self._currentFileTupleIndex = 0
        self._imageSlider = None
        self.initUi()

    def initUi(self) -> None:
        # Init graphics canvas
        self._graphicsView = QGraphicsView(self)
        self._scene = QGraphicsScene(self)
        item = self._scene.addText('DICOM Viewer')
        item.setDefaultTextColor(Qt.blue)
        self._graphicsView.setScene(self._scene)
        # Image slider
        self._imageSlider = QSlider(Qt.Horizontal, self)
        self._imageSlider.setRange(0, 100)
        self._imageSlider.valueChanged.connect(self.currentImageIndexChanged)
        # Init layout
        layout = QVBoxLayout()
        layout.addWidget(self._graphicsView)
        layout.addWidget(self._imageSlider)
        # layout.addWidget(self._segmentationMaskOpacitySlider)
        self.setLayout(layout)

    def findNumPyFileForDicomFile(self, dicomFile: File, fileSet: FileSet) -> File:
        for file in fileSet.files():
            if file.name() == dicomFile.name() + '.seg':
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
        for file in fileSet.files():
            fileTuple = [None, None, None, None] # [DICOM File, pydicom.FileModel, NumPy File, TAG File]
            if isDicomFile(filePath=file.path()):
                fileTuple[0] = file
                dicomFile = pydicom.dcmread(file.path())
                dicomFile.decompress()
                fileTuple[1] = dicomFile
                numpyFile = self.findNumPyFileForDicomFile(dicomFile=file, fileSet=fileSet)
                if numpyFile:
                    fileTuple[2] = numpyFile
                    # fileTuple[3] = np.load(numpyFile.path())
                tagFile = self.findTagFileForDicomFile(dicomFile=file, fileSet=fileSet)
                if tagFile:
                    fileTuple[3] = tagFile
                    # fileTuple[5] = tagPixels(tagFilePath=tagFile.path())
                self._fileTuples.append(fileTuple)
        self._fileTuples = sorted(self._fileTuples, key=lambda fileTuple: fileTuple[1].InstanceNumber)
        self.displayFileTuple(self._currentFileTupleIndex)

    def currentImageIndexChanged(self, index) -> None:
        pass

    def wheelEvent(self, event) -> None:
        delta = event.angleDelta().y()
        # if delta > 0 and self._currentImageIndex > 0:
        #     self._currentImageIndex -= 1
        # elif delta < 0 and self._currentImageIndex < len(self._dicomViewerImages) - 1:
        #     self._currentImageIndex += 1
        # self._imageSlider.valueChanged.disconnect(self.currentImageIndexChanged)
        # self._imageSlider.setValue(self._currentImageIndex)
        # self._imageSlider.valueChanged.connect(self.currentImageIndexChanged)
        # self.displayDicomViewerImage(self._currentImageIndex)
        pass

    def displayFileTuple(self, index: int) -> None:
        if len(self._fileTuples) > 0 and index < len(self._fileTuples):
            fileTuple = self._fileTuples[index]
            self._scene.clear()
            # self._scene.addItem(dicomViewerImage.dicomFileLayer().createGraphicsItem())
