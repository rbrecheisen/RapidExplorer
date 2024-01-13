import os
import shutil
import pydicom
import pydicom.errors
import pandas as pd
import numpy as np

from typing import List, Dict

from tasks.task import Task
from data.file import File
from data.filecontent import FileContent
from data.filecontentcache import FileContentCache
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

    def findSegmentationFileForDicomFile(self, dicomFile: File, segmentationFiles: List[File]) -> File:
        for segmentationFile in segmentationFiles:
            segmentationFilePath = segmentationFile.path()
            segmentationFileName = os.path.split(segmentationFilePath)[1]
            if dicomFile.name() + '.seg.npy' == segmentationFileName:
                return segmentationFile
        return None

    def findTagFileForDicomFile(self, dicomFile, files: List[File]) -> File:
        tagFilePath1 = dicomFile.path() + '.tag'
        tagFilePath2 = dicomFile.path()[:-4] + '.tag'
        for file in files:            
            if file.path() == tagFilePath1:
                return file
            if file.path() == tagFilePath2:
                return file    
        return None

    def loadDicomFile(self, file: str):
        content = self.readFromCache(file=file)
        if not content:
            p = pydicom.dcmread(file.path())
            p.decompress()
            content = self.writeToCache(file, p)
        p = content.fileObject()
        pixelSpacing = p.PixelSpacing
        pixels = getPixelsFromDicomObject(p, normalize=True)
        return pixels, pixelSpacing

    def loadSegmentationFile(self, file: str):
        content = self.readFromCache(file=file.path())
        if not content:
            labels = np.load(file)
            content = self.writeToCache(file, labels)
        labels = content.fileObject()
        return labels
    
    def loadTagFile(self, file: str, shape: List[int]):
        content = self.readFromCache(file=file.path())
        if not content:
            labels = tagPixels(tagFilePath=file.path())
            content = self.writeToCache(file, labels)
        labels = content.fileObject()
        return labels.reshape(shape)
    
    def fileOutputMetricsToString(self, outputMetrics: Dict[str, float], fileName: str) -> None:
        text = fileName + ':\n'
        for metric, value in outputMetrics.items():
            text += f'  - {metric}: {value}\n'
        self.addInfo(text)

    def execute(self) -> None:
        # Get input DICOM fileset
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        if inputFileSet:            
            self.addInfo(f'Input fileset: {inputFileSet.path()}')

            # Get input segmentation fileset
            inputSegmentationFileSetName = self.parameter('inputSegmentationFileSetName').value()
            inputSegmentationFileSet = self.dataManager().fileSetByName(inputSegmentationFileSetName)
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
                fileTuples = []
                outputMetrics = {} # Contains BC metrics
                for file in files:

                    # Check if task was canceled first
                    if self.statusIsCanceled():
                        self.addInfo('Canceling task...')
                        break

                    fileTuple = [None, None, None]

                    if isDicomFile(filePath=file.path()):
                        fileTuple[0] = file.path()

                        # Try to find TAG file
                        tagFile = self.findTagFileForDicomFile(dicomFile=file, files=files)
                        if tagFile:
                            fileTuple[2] = tagFile

                        # Get segmentation file for DICOM file
                        segmentationFile = self.findSegmentationFileForDicomFile(dicomFile=file, segmentationFiles=inputSegmentationFileSet.files())
                        if segmentationFile:
                            fileTuple[1] = segmentationFile
                            fileTuples.append(fileTuple)

                            # Get DICOM pixels, pixel spacing, predicted segmentation labels and TAG labels if available
                            image, pixelSpacing = self.loadDicomFile(file=fileTuple[0])
                            segmentation = self.loadSegmentationFile(file=fileTuple[1])
                            
                            # Calculate metrics for predicted segmentation
                            outputMetrics[fileTuple[0]] = {}
                            outputMetrics[fileTuple[0]]['file'] = fileTuple[0]
                            outputMetrics[fileTuple[0]]['muscle_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.MUSCLE, pixelSpacing)
                            outputMetrics[fileTuple[0]]['vat_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.VAT, pixelSpacing)
                            outputMetrics[fileTuple[0]]['sat_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.SAT, pixelSpacing)
                            outputMetrics[fileTuple[0]]['muscle_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.MUSCLE)
                            outputMetrics[fileTuple[0]]['vat_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.VAT)
                            outputMetrics[fileTuple[0]]['sat_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.SAT)

                            if tagFile:
                                # Calculate metrics for true segmentation based on TAG file
                                tagImage = self.loadTagFile(file=fileTuple[2], shape=image.shape)
                                outputMetrics[fileTuple[0]]['muscle_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.MUSCLE, pixelSpacing)
                                outputMetrics[fileTuple[0]]['vat_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.VAT, pixelSpacing)
                                outputMetrics[fileTuple[0]]['sat_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.SAT, pixelSpacing)
                                outputMetrics[fileTuple[0]]['muscle_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.MUSCLE)
                                outputMetrics[fileTuple[0]]['vat_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.VAT)
                                outputMetrics[fileTuple[0]]['sat_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.SAT)

                            self.addInfo(self.fileOutputMetricsToString(outputMetrics=outputMetrics[fileTuple[0]]))
                        else:
                            self.addError(f'Segmentation file {segmentationFile.name()} not found')                        
                
                    # Update progress based on nr. steps required. This will automatically
                    # send sigals/events to the task widget
                    self.updateProgress(step=step, nrSteps=nrSteps)
                    step += 1
                
                # Build output fileset using Pandas
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

                # Create new output fileset from the CSV file. No need to cache it because it's just
                # text and we're probably not going to use it further
                self.dataManager().createFileSet(fileSetPath=outputFileSetPath)

                # Update final progress
                self.updateProgress(step=step, nrSteps=nrSteps)
                self.addInfo('Finished')                
            else:
                self.addError(f'Segmentation fileset {inputSegmentationFileSetName} not found')
        else:
            self.addError(f'Input fileset {inputFileSetName} not found')