import os
import pydicom
import pydicom.errors
import numpy as np
import pandas as pd

from typing import List, Dict

from utils import getPixelsFromDicomObject, calculateArea, calculateMeanRadiationAttennuation
from logger import Logger

LOGGER = Logger('MosamaticDesktop')


class BodyCompositionValidationCalculator:
    MUSCLE = 1
    VAT = 5
    SAT = 7

    def __init__(self, parentTask):
        self._parentTask = parentTask
        self._dicomAndTagFilePaths = None
        self._segmentationFilePaths = None
        self._patientHeights = {}
        self._outputMetrics = None
        self._progress = 0

    def dicomAndTagFilePaths(self) -> List[str]:
        return self._dicomAndTagFilePaths
    
    def setDicomAndTagFilePaths(self, dicomAndTagFilePaths: List[str]) -> None:
        self._dicomAndTagFilePaths = dicomAndTagFilePaths

    def segmentationFilePaths(self) -> List[str]:
        return self._segmentationFilePaths
    
    def setSegmentationFilePaths(self, segmentationFilePaths: List[str]) -> None:
        self._segmentationFilePaths = segmentationFilePaths

    def patientHeights(self) -> Dict[str, float]:
        return self._patientHeights
    
    def setPatientHeights(self, patientHeights: Dict[str, float]) -> None:
        self._patientHeights = patientHeights

    @staticmethod
    def loadDicomFile(filePath: str):
        p = pydicom.dcmread(filePath)
        pixelSpacing = p.PixelSpacing
        pixels = getPixelsFromDicomObject(p, normalize=True)
        return pixels, pixelSpacing

    @staticmethod
    def loadSegmentation(filePath: str):
        return np.load(filePath)
    
    def isDicomFile(self, filePath: str) -> bool:
        try:
            pydicom.dcmread(filePath, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False

    def tagFilePathForDicomFilePath(self, filePath: str) -> bool:
        return filePath.endswith('.tag')
    
    def execute(self):
        fileTuples = []
        for dicomAndTagFilePath in self.dicomAndTagFilePaths():
            dicomFilePath = None
            tagFilePath = None
            if self.isDicomFile(filePath=dicomAndTagFilePath):
                dicomFilePath = dicomAndTagFilePath
            tagFilePath = self.tagFilePathForDicomFilePath(filePath=dicomAndTagFilePath):
            if not tagFilePath:
                LOGGER.error(f'Could not find TAG file for {dicomFilePath}')
                continue
            segmentationFilePath = None
            dicomFileName = os.path.split(dicomFilePath)[1]
            for filePath in self.segmentationFilePaths():
                fileName = os.path.split(filePath)[1]
                if dicomFileName + '.seg.npy' == fileName:
                    segmentationFilePath = filePath
                    break
            if dicomFilePath and tagFilePath and segmentationFilePath:
                fileTuples.append((dicomFilePath, tagFilePath, segmentationFilePath))
            else:
                raise RuntimeError('Could not find tuple (dicomFilePath, tagFilePath, segmentationFilePath)')
        # Work with found file tuples
        self.outputMetrics = {}
        for filePair in fileTuples:
            image, pixelSpacing = self.loadDicomFile(filePair[0])
            segmentations = self.loadSegmentation(filePair[1])
            self.outputMetrics[filePair[0]] = {}
            self.outputMetrics[filePair[0]] = {
                'muscle_area': calculateArea(segmentations, BodyCompositionCalculator.MUSCLE, pixelSpacing),
                'vat_area': calculateArea(segmentations, BodyCompositionCalculator.VAT, pixelSpacing),
                'sat_area': calculateArea(segmentations, BodyCompositionCalculator.SAT, pixelSpacing),
                'muscle_ra': calculateMeanRadiationAttennuation(image, segmentations, BodyCompositionCalculator.MUSCLE),
                'vat_ra': calculateMeanRadiationAttennuation(image, segmentations, BodyCompositionCalculator.VAT),
                'sat_ra': calculateMeanRadiationAttennuation(image, segmentations, BodyCompositionCalculator.SAT),
            }
            print(f'{filePair[0]}')
            print(' - muscle_area: {}'.format(self.outputMetrics[filePair[0]]['muscle_area']))
            print(' - vat_area: {}'.format(self.outputMetrics[filePair[0]]['vat_area']))
            print(' - sat_area: {}'.format(self.outputMetrics[filePair[0]]['sat_area']))
            print(' - muscle_ra: {}'.format(self.outputMetrics[filePair[0]]['muscle_ra']))
            print(' - vat_ra: {}'.format(self.outputMetrics[filePair[0]]['vat_ra']))
            print(' - sat_ra: {}'.format(self.outputMetrics[filePair[0]]['sat_ra']))
            self._progress += 1
            self._parentTask.calculatorProgress(self._progress)
        return self.outputMetrics
    
    def as_df(self):
        if self.outputMetrics is None:
            return None
        data = {'file': [], 'muscle_area': [], 'vat_area': [], 'sat_area': [], 'muscle_ra': [], 'vat_ra': [], 'sat_ra': []}
        for k in self.outputMetrics.keys():
            data['file'].append(k)
            data['muscle_area'].append(self.outputMetrics[k]['muscle_area'])
            data['vat_area'].append(self.outputMetrics[k]['vat_area'])
            data['sat_area'].append(self.outputMetrics[k]['sat_area'])
            data['muscle_ra'].append(self.outputMetrics[k]['muscle_ra'])
            data['vat_ra'].append(self.outputMetrics[k]['vat_ra'])
            data['sat_ra'].append(self.outputMetrics[k]['sat_ra'])
        return pd.DataFrame(data=data)