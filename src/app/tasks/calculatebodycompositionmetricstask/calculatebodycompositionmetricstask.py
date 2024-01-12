import os
import shutil
import pydicom
import pydicom.errors
import pandas as pd
import numpy as np

from typing import List, Dict

from tasks.task import Task
from data.file import File
from utils import getPixelsFromDicomObject, tagPixels, isDicomFile, calculateArea
from utils import calculateMeanRadiationAttennuation, createNameWithTimestamp
from logger import Logger

LOGGER = Logger()


class CalculateBodyCompositionMetricsTaskTask(Task):
    MUSCLE = 1
    VAT = 5
    SAT = 7

    def __init__(self) -> None:
        super(CalculateBodyCompositionMetricsTaskTask, self).__init__()

    def findSegmentationFilePathForDicomFile(self, dicomFile: File, segmentationFiles: List[File]) -> str:
        for segmentationFile in segmentationFiles:
            segmentationFilePath = segmentationFile.path()
            segmentationFileName = os.path.split(segmentationFilePath)[1]
            if dicomFile.name() + '.seg.npy' == segmentationFileName:
                return segmentationFilePath
        return None

    def findTagFilePathForDicomFile(self, dicomFile) -> str:
        tagFilePath = dicomFile.path() + '.tag'
        if os.path.isfile(tagFilePath):
            return tagFilePath
        tagFilePath = dicomFile.path()[:-4] + '.tag'
        if os.path.isfile(tagFilePath):
            return tagFilePath
        return None

    def loadDicomFile(self, filePath: str):
        p = pydicom.dcmread(filePath)
        pixelSpacing = p.PixelSpacing
        pixels = getPixelsFromDicomObject(p, normalize=True)
        return pixels, pixelSpacing

    def loadSegmentationFile(self, filePath: str):
        return np.load(filePath)
    
    def loadTagFile(self, filePath: str):
        return tagPixels(tagFilePath=filePath)
    
    def printOutputMetricsForFile(self, outputMetricsForFile: Dict[str, float], filePath: str) -> None:
        LOGGER.info(filePath)
        LOGGER.info(outputMetricsForFile)

    def execute(self) -> None:
        # Get input DICOM fileset
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        if inputFileSet:            
            self.addInfo(f'Input fileset: {inputFileSet.path()}')

            # Get input segmentation fileset
            inputSegmentationFileSetName = self.parameter('inputSegmentationFileSetName').value()
            inputSegmentationFileSet = manager.fileSetByName(inputSegmentationFileSetName)
            if inputSegmentationFileSet:
                self.addInfo(f'Input segmentation fileset: {inputSegmentationFileSet.path()}')

                # Get CSV file with patient heights
                patientHeightsCsvFilePath = self.parameter('patientHeightsCsvFilePath').value()
                if patientHeightsCsvFilePath and patientHeightsCsvFilePath != '':
                    self.addInfo(f'Patient Height CSV file: {patientHeightsCsvFilePath}')
                    patientHeightsDataFrame = pd.read_csv(patientHeightsCsvFilePath)

                # Get output fileset path
                outputFileSetName = self.parameter('outputFileSetName').value()
                if not outputFileSetName:
                    outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
                self.addInfo(f'Output fileset name: {outputFileSetName}')

                # Get output fileset path
                outputFileSetPath = self.parameter('outputFileSetPath').value()
                outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
                self.addInfo(f'Output fileset: {outputFileSetPath}')

                # Remove old output fileset directory if needed
                overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
                if overwriteOutputFileSet:
                    if os.path.isdir(outputFileSetPath):
                        shutil.rmtree(outputFileSetPath)
                os.makedirs(outputFileSetPath, exist_ok=False)

                files = inputFileSet.files()
                nrSteps = len(files) + 1
                step = 0
                filePathTuples = []
                outputMetrics = {} # Contains BC metrics
                for file in files:

                    # Check if task was canceled first
                    if self.statusIsCanceled():
                        self.addInfo('Canceling task...')
                        break

                    filePathTuple = [None, None, None]

                    if isDicomFile(filePath=file.path()):
                        filePathTuple[0] = file.path()

                        # Try to find TAG file
                        tagFilePath = self.findTagFilePathForDicomFile(dicomFile=file)
                        if tagFilePath:
                            filePathTuple[2] = tagFilePath

                        # Get segmentation file for DICOM file
                        segmentationFilePath = self.findSegmentationFilePathForDicomFile(dicomFile=file, segmentationFiles=inputSegmentationFileSet.files())
                        if segmentationFilePath:
                            filePathTuple[1] = segmentationFilePath
                            filePathTuples.append(filePathTuple)

                            # Get DICOM pixels, pixel spacing, predicted segmentation labels and TAG labels if available
                            image, pixelSpacing = self.loadDicomFile(filePath=filePathTuple[0])
                            segmentation = self.loadSegmentationFile(filePath=filePathTuple[1])
                            
                            # Calculate metrics for predicted segmentation
                            outputMetrics[filePathTuple[0]] = {}
                            outputMetrics[filePathTuple[0]]['file'] = filePathTuple[0]
                            outputMetrics[filePathTuple[0]]['muscle_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.MUSCLE, pixelSpacing)
                            outputMetrics[filePathTuple[0]]['vat_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.VAT, pixelSpacing)
                            outputMetrics[filePathTuple[0]]['sat_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.SAT, pixelSpacing)
                            outputMetrics[filePathTuple[0]]['muscle_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.MUSCLE)
                            outputMetrics[filePathTuple[0]]['vat_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.VAT)
                            outputMetrics[filePathTuple[0]]['sat_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.SAT)

                            if tagFilePath:
                                # Calculate metrics for true segmentation based on TAG file
                                tagImage = self.loadTagFile(filePath=filePathTuple[2])
                                outputMetrics[filePathTuple[0]]['muscle_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.MUSCLE, pixelSpacing)
                                outputMetrics[filePathTuple[0]]['vat_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.VAT, pixelSpacing)
                                outputMetrics[filePathTuple[0]]['sat_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.SAT, pixelSpacing)
                                outputMetrics[filePathTuple[0]]['muscle_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.MUSCLE)
                                outputMetrics[filePathTuple[0]]['vat_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.VAT)
                                outputMetrics[filePathTuple[0]]['sat_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.SAT)
                        else:
                            self.addError(f'Segmentation file {segmentationFilePath.name()} not found')                        
                
                    # Update progress based on nr. steps required. This will automatically
                    # send sigals/events to the task widget
                    self.updateProgress(step=step, nrSteps=nrSteps)
                    step += 1
                
                # Build output fileset
                self.addInfo(f'Building output fileset: {outputFileSetPath}...')
                firstKey = next(iter(outputMetrics))
                columns = list(outputMetrics[firstKey].keys())
                data = {}
                for column in columns:
                    data[column] = []
                for filePath in outputMetrics.keys():
                    for column in columns:
                        data[column].append(outputMetrics[filePath][column])
                csvFilePath = os.path.join(outputFileSetPath, createNameWithTimestamp('scores') + '.csv')
                df = pd.DataFrame(data=data)
                df.to_csv(csvFilePath, index=False)

                self.dataManager().createFileSet(fileSetPath=outputFileSetPath)

                # Update final progress
                self.updateProgress(step=step, nrSteps=nrSteps)
                self.addInfo('Finished')                
            else:
                self.addError(f'Segmentation fileset {inputSegmentationFileSetName} not found')
        else:
            self.addError(f'Input fileset {inputFileSetName} not found')