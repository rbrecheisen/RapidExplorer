import os
import json
import zipfile
import pydicom
import pydicom.errors
import numpy as np

from typing import List

from PySide6.QtCore import QSettings

from utils import getPixelsFromDicomObject, SettingsIniFile, convertLabelsTo157, normalizeBetween

# SETTINGSFILEPATH = os.environ.get('SETTINGSPATH', 'settings.ini')
SETTINGSFILEPATH = SettingsIniFile().path()


class MuscleFatSegmentor:
    ARGMAX = 0
    PROBABILITIES = 1

    def __init__(self, parentTask) -> None:
        self._parentTask = parentTask
        self._inputFiles = None
        self._modelFiles = None
        self._mode = MuscleFatSegmentor.ARGMAX
        self._outputDirectory = None
        self._outputFiles = None
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self._progress = 0

    def inputFiles(self) -> List[str]:
        return self._inputFiles
    
    def setInputFiles(self, inputFiles: List[str]) -> None:
        self._inputFiles = inputFiles

    def modelFiles(self) -> List[str]:
        return self._modelFiles
    
    def setModelFiles(self, modelFiles: List[str]) -> None:
        self._modelFiles = modelFiles

    def mode(self) -> int:
        return self._mode
    
    def setMode(self, mode: int) -> None:
        if mode != 0 and mode != 1:
            raise RuntimeError('Modes allowed: 0 (ARGMAX) or 1 (PROBABILITIES)')
        self._mode = mode

    def outputDirectory(self) -> str:
        return self._outputDirectory
    
    def setOutputDirectory(self, outputDirectory: str) -> None:
        self._outputDirectory = outputDirectory

    def outputFiles(self) -> List[str]:
        return self._outputFiles

    def settings(self) -> QSettings:
        return self._settings
    
    def updateProgress(self) -> int:
        self._progress += 1
        self._parentTask.segmentorProgress(self._progress)
    
    def loadModel(self, filePath: str):
        import tensorflow as tf
        temporaryModelDirectory = self.settings().value('MuscleFatSegmentationTaskTemporaryModelDirectory')
        os.makedirs(temporaryModelDirectory, exist_ok=True)
        with zipfile.ZipFile(filePath) as zipObj:
            zipObj.extractall(path=temporaryModelDirectory)
        tensorFlowModel = tf.keras.models.load_model(temporaryModelDirectory, compile=False)
        return tensorFlowModel

    def loadParameters(self, filePath: str):
        with open(filePath, 'r') as f:
            parameters = json.load(f)
            return parameters

    def loadModelFiles(self):
        model, contourModel, parameters = None, None, None
        for filePath in self.modelFiles():
            fileName = os.path.split(filePath)[1]
            if fileName == 'model.zip':
                model = self.loadModel(filePath)
            elif fileName == 'contour_model.zip':
                contourModel = self.loadModel(filePath)
            elif fileName == 'params.json':
                parameters = self.loadParameters(filePath)
            else:
                raise RuntimeError(f'Unknown model file {filePath}')
            self.updateProgress()
        return model, contourModel, parameters
    
    def predictContour(self, contourModel, sourceImage, parameters):
        ct = np.copy(sourceImage)
        ct = normalizeBetween(ct, parameters['min_bound_contour'], parameters['max_bound_contour'])
        img2 = np.expand_dims(ct, 0)
        img2 = np.expand_dims(img2, -1)
        pred = contourModel.predict([img2])
        predSqueeze = np.squeeze(pred)
        pred_max = predSqueeze.argmax(axis=-1)
        mask = np.uint8(pred_max)
        return mask

    def execute(self) -> List[str]:
        model, contourModel, params = self.loadModelFiles()
        self._outputFiles = []
        for filePath in self.inputFiles():
            fileName = os.path.split(filePath)[1]
            try:
                p = pydicom.dcmread(filePath)
                p.decompress()
                img1 = getPixelsFromDicomObject(p, normalize=True)
                if contourModel is not None:
                    mask = self.predictContour(contourModel, img1, params)
                    img1 = normalizeBetween(img1, params['min_bound'], params['max_bound'])
                    img1 = img1 * mask
                else:
                    img1 = normalizeBetween(img1, params['min_bound'], params['max_bound'])
                img1 = img1.astype(np.float32)
                img2 = np.expand_dims(img1, 0)
                img2 = np.expand_dims(img2, -1)
                pred = model.predict([img2])
                predSqueeze = np.squeeze(pred)
                if self.mode() == MuscleFatSegmentor.ARGMAX:
                    predMax = predSqueeze.argmax(axis=-1)
                    predMax = convertLabelsTo157(predMax)
                    segmentationFile = os.path.join(self.outputDirectory(), f'{fileName}.seg.npy')
                    self._outputFiles.append(segmentationFile)
                    np.save(segmentationFile, predMax)
                elif self.mode() == MuscleFatSegmentor.PROBABILITIES:
                    segmentationFile = os.path.join(self.outputDirectory(), f'{fileName}.seg.prob.npy')
                    self._outputFiles.append(segmentationFile)
                    np.save(segmentationFile, predSqueeze)
            except pydicom.errors.InvalidDicomError:
                print(f'File {fileName} is not a valid DICOM file')
            self.updateProgress()
        return self._outputFiles