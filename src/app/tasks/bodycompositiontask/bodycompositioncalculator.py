import os
import pydicom
import numpy as np
import pandas as pd

from typing import List

from tasks.utils import calculate_area, calculate_mean_radiation_attenuation


class BodyCompositionCalculator:
    MUSCLE = 1
    VAT = 5
    SAT = 7

    def __init__(self, parentTask):
        self._parentTask = parentTask
        self._inputFiles = None
        self._inputSegmentationFiles = None
        self._heights = {}
        self._outputMetrics = None

    def inputFiles(self) -> List[str]:
        return self._inputFiles
    
    def setInputFiles(self, inputFiles: List[str]) -> None:
        self._inputFiles = inputFiles

    def inputSegmentationFiles(self) -> List[str]:
        return self._inputSegmentationFiles
    
    def setInputSegmentationFiles(self, inputSegmentationFiles: List[str]) -> None:
        self._inputSegmentationFiles = inputSegmentationFiles

    def heights(self) -> Dict[str, float]:
        return self._heights
    
    def setHeights(self, heights: Dict[str, float]) -> None:
        self._heights = heights

    @staticmethod
    def loadDicomFile(filePath: str):
        p = pydicom.dcmread(filePath)
        pixelSpacing = p.PixelSpacing
        pixels = get_pixels(p, normalize=True)
        return pixels, pixelSpacing

    @staticmethod
    def loadSegmentation(filePath: str):
        return np.load(filePath)
    
    def execute(self):
        file_pairs = []
        for input_file in self.inputFiles:
            input_file_name = os.path.split(input_file)[1]
            for input_segmentation_file in self.inputSegmentationFiles:
                input_segmentation_file_name = os.path.split(input_segmentation_file)[1]
                if input_file_name + '.seg.npy' == input_segmentation_file_name:
                    file_pairs.append((input_file, input_segmentation_file))
                    break
        # Work with found file pairs
        self.outputMetrics = {}
        for file_pair in file_pairs:
            image, pixel_spacing = self.loadDicomFile(file_pair[0])
            segmentations = self.loadSegmentation(file_pair[1])
            self.outputMetrics[file_pair[0]] = {}
            self.outputMetrics[file_pair[0]] = {
                'muscle_area': calculate_area(segmentations, BodyCompositionCalculator.MUSCLE, pixel_spacing),
                'vat_area': calculate_area(segmentations, BodyCompositionCalculator.VAT, pixel_spacing),
                'sat_area': calculate_area(segmentations, BodyCompositionCalculator.SAT, pixel_spacing),
                'muscle_ra': calculate_mean_radiation_attenuation(image, segmentations, BodyCompositionCalculator.MUSCLE),
                'vat_ra': calculate_mean_radiation_attenuation(image, segmentations, BodyCompositionCalculator.VAT),
                'sat_ra': calculate_mean_radiation_attenuation(image, segmentations, BodyCompositionCalculator.SAT),
            }
            print(f'{file_pair[0]}')
            print(' - muscle_area: {}'.format(self.outputMetrics[file_pair[0]]['muscle_area']))
            print(' - vat_area: {}'.format(self.outputMetrics[file_pair[0]]['vat_area']))
            print(' - sat_area: {}'.format(self.outputMetrics[file_pair[0]]['sat_area']))
            print(' - muscle_ra: {}'.format(self.outputMetrics[file_pair[0]]['muscle_ra']))
            print(' - vat_ra: {}'.format(self.outputMetrics[file_pair[0]]['vat_ra']))
            print(' - sat_ra: {}'.format(self.outputMetrics[file_pair[0]]['sat_ra']))
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