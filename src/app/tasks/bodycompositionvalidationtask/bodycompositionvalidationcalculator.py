import os
import pydicom
import pydicom.errors
import numpy as np
import pandas as pd

from typing import List, Dict

from utils import getPixelsFromDicomObject, calculateArea, calculateMeanRadiationAttennuation, tagPixels
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
    
    @staticmethod
    def loadTagFile(filePath: str, shape=(512, 512)):
        pixels = tagPixels(tagFilePath=filePath)
        return pixels.reshape(shape)
    
    @staticmethod
    def isDicomFile(filePath: str) -> bool:
        try:
            pydicom.dcmread(filePath, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False

    @staticmethod
    def tagFilePathForDicomFilePath(filePath: str) -> bool:
        if os.path.isfile(filePath + '.tag'):
            return filePath + '.tag'
        elif os.path.isfile(filePath[:-4] + '.tag'):
            return filePath[:-4] + '.tag'
        return None
    
    def execute(self):
        fileTuples = []
        for dicomAndTagFilePath in self.dicomAndTagFilePaths():
            dicomFilePath = None
            tagFilePath = None
            segmentationFilePath = None
            if self.isDicomFile(filePath=dicomAndTagFilePath):
                dicomFilePath = dicomAndTagFilePath
                tagFilePath = self.tagFilePathForDicomFilePath(filePath=dicomFilePath)
                if tagFilePath:
                    segmentationFilePath = None
                    dicomFileName = os.path.split(dicomFilePath)[1]
                    for filePath in self.segmentationFilePaths():
                        fileName = os.path.split(filePath)[1]
                        if dicomFileName + '.seg.npy' == fileName:
                            segmentationFilePath = filePath
                            break
                    if segmentationFilePath:
                        fileTuples.append((dicomFilePath, tagFilePath, segmentationFilePath))
        # Work with found file tuples
        self.outputMetrics = {}
        for fileTuple in fileTuples:
            image, pixelSpacing = self.loadDicomFile(fileTuple[0])
            groundTruthSegmentations = self.loadTagFile(fileTuple[1], shape=image.shape)
            segmentations = self.loadSegmentation(fileTuple[2])
            self.outputMetrics[fileTuple[0]] = {}
            self.outputMetrics[fileTuple[0]] = {
                'muscle_area_true': calculateArea(groundTruthSegmentations, BodyCompositionValidationCalculator.MUSCLE, pixelSpacing),
                'muscle_area_pred': calculateArea(segmentations, BodyCompositionValidationCalculator.MUSCLE, pixelSpacing),
                'vat_area_true': calculateArea(groundTruthSegmentations, BodyCompositionValidationCalculator.VAT, pixelSpacing),
                'vat_area_pred': calculateArea(segmentations, BodyCompositionValidationCalculator.VAT, pixelSpacing),
                'sat_area_true': calculateArea(groundTruthSegmentations, BodyCompositionValidationCalculator.SAT, pixelSpacing),
                'sat_area_pred': calculateArea(segmentations, BodyCompositionValidationCalculator.SAT, pixelSpacing),
                'muscle_ra_true': calculateMeanRadiationAttennuation(image, groundTruthSegmentations, BodyCompositionValidationCalculator.MUSCLE),
                'muscle_ra_pred': calculateMeanRadiationAttennuation(image, segmentations, BodyCompositionValidationCalculator.MUSCLE),
                'vat_ra_true': calculateMeanRadiationAttennuation(image, groundTruthSegmentations, BodyCompositionValidationCalculator.VAT),
                'vat_ra_pred': calculateMeanRadiationAttennuation(image, segmentations, BodyCompositionValidationCalculator.VAT),
                'sat_ra_true': calculateMeanRadiationAttennuation(image, groundTruthSegmentations, BodyCompositionValidationCalculator.SAT),
                'sat_ra_pred': calculateMeanRadiationAttennuation(image, segmentations, BodyCompositionValidationCalculator.SAT),
            }
            print(f'{fileTuple[0]}')
            print(' - muscle_area: true={} <-> predicted={}'.format(
                self.outputMetrics[fileTuple[0]]['muscle_area_true'],
                self.outputMetrics[fileTuple[0]]['muscle_area_pred']
                ))
            print(' - vat_area: true={} <-> predicted={}'.format(
                self.outputMetrics[fileTuple[0]]['vat_area_true'],
                self.outputMetrics[fileTuple[0]]['vat_area_pred']
                ))
            print(' - sat_area: true={} <-> predicted={}'.format(
                self.outputMetrics[fileTuple[0]]['sat_area_true'],
                self.outputMetrics[fileTuple[0]]['sat_area_pred']
                ))
            print(' - muscle_ra: true={} <-> predicted={}'.format(
                self.outputMetrics[fileTuple[0]]['muscle_ra_true'],
                self.outputMetrics[fileTuple[0]]['muscle_ra_pred']
                ))
            print(' - vat_ra: true={} <-> predicted={}'.format(
                self.outputMetrics[fileTuple[0]]['vat_ra_true'],
                self.outputMetrics[fileTuple[0]]['vat_ra_pred']
                ))
            print(' - sat_ra: true={} <-> predicted={}'.format(
                self.outputMetrics[fileTuple[0]]['sat_ra_true'],
                self.outputMetrics[fileTuple[0]]['sat_ra_pred']
                ))
            self._progress += 1
            self._parentTask.calculatorProgress(self._progress)
        return self.outputMetrics
    
    def as_df(self):
        if self.outputMetrics is None:
            return None
        data = {
            'file': [], 
            'muscle_area_true': [], 'muscle_area_pred': [], 
            'vat_area_true': [], 'vat_area_pred': [],
            'sat_area_true': [], 'sat_area_pred': [],
            'muscle_ra_true': [], 'muscle_ra_pred': [],
            'vat_ra_true': [], 'vat_ra_pred': [],
            'sat_ra_true': [], 'sat_ra_pred': [],
        }
        for k in self.outputMetrics.keys():
            data['file'].append(k)
            data['muscle_area_true'].append(self.outputMetrics[k]['muscle_area_true'])
            data['muscle_area_pred'].append(self.outputMetrics[k]['muscle_area_pred'])
            data['vat_area_true'].append(self.outputMetrics[k]['vat_area_true'])
            data['vat_area_pred'].append(self.outputMetrics[k]['vat_area_pred'])
            data['sat_area_true'].append(self.outputMetrics[k]['sat_area_true'])
            data['sat_area_pred'].append(self.outputMetrics[k]['sat_area_pred'])
            data['muscle_ra_true'].append(self.outputMetrics[k]['muscle_ra_true'])
            data['muscle_ra_pred'].append(self.outputMetrics[k]['muscle_ra_pred'])
            data['vat_ra_true'].append(self.outputMetrics[k]['vat_ra_true'])
            data['vat_ra_pred'].append(self.outputMetrics[k]['vat_ra_pred'])
            data['sat_ra_true'].append(self.outputMetrics[k]['sat_ra_true'])
            data['sat_ra_pred'].append(self.outputMetrics[k]['sat_ra_pred'])
        return pd.DataFrame(data=data)