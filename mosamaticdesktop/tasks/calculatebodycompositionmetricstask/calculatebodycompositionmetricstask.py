import os
import shutil
import pydicom
import pydicom.errors
import pandas as pd
import numpy as np

from typing import List, Dict

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.data.file import File
from mosamaticdesktop.utils import getPixelsFromDicomObject, tagPixels, isDicomFile, calculateArea, calculateIndex, calculateDiceScore
from mosamaticdesktop.utils import calculateMeanRadiationAttennuation, createNameWithTimestamp, readFromCache, writeToCache
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class CalculateBodyCompositionMetricsTaskTask(Task):
    MUSCLE = 1
    VAT = 5
    SAT = 7

    def __init__(self) -> None:
        super(CalculateBodyCompositionMetricsTaskTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Calculates body composition metrics on predicted segmenations and TAG files if available'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input DICOM (and TAG) File Set',
        )
        self.addFileSetParameter(
            name='inputSegmentationFileSetName',
            labelText='Input Segmentation File Set',
        )
        self.addPathParameter(
            name='patientHeightsCsvFilePath',
            labelText='Patient Height CSV File Path (File Name, Height (m))',
            optional=True,
        )
        self.addPathParameter(
            name='outputFileSetPath',
            labelText='Output File Set Path',
        )
        self.addTextParameter(
            name='outputFileSetName',
            labelText='Output File Set Name',
            optional=True,
        )
        self.addBooleanParameter(
            name='overwriteOutputFileSet',
            labelText='Overwrite Output File Set',
            defaultValue=True,
        )

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

    def loadDicomFile(self, file: File):
        content = readFromCache(file=file)
        if not content:
            p = pydicom.dcmread(file.path())
            p.decompress()
            content = writeToCache(file, p)
        p = content.fileObject()
        pixelSpacing = p.PixelSpacing
        pixels = getPixelsFromDicomObject(p, normalize=True)
        return pixels, pixelSpacing

    def loadSegmentationFile(self, file: File):
        content = readFromCache(file=file)
        if not content:
            labels = np.load(file.path())
            content = writeToCache(file, labels)
        labels = content.fileObject()
        return labels
    
    def loadTagFile(self, file: File, shape: List[int]):
        content = readFromCache(file=file)
        if not content:
            labels = tagPixels(tagFilePath=file.path())
            content = writeToCache(file, labels)
        labels = content.fileObject()
        return labels.reshape(shape)
    
    def loadPatientHeights(self, df: pd.DataFrame) -> Dict[str, float]:
        data = {}
        for idx, row in df.iterrows():
            data['file'] = row['file']
            data['height'] = row['height']
        return data
    
    def fileOutputMetricsToString(self, outputMetrics: Dict[str, float]) -> None:
        text = ''
        for metric, value in outputMetrics.items():
            text += f'  - {metric}: {value}\n'
        self.addInfo(text)

    def execute(self) -> None:
        # Get input parameters
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        inputSegmentationFileSetName = self.parameter('inputSegmentationFileSetName').value()
        inputSegmentationFileSet = self.dataManager().fileSetByName(inputSegmentationFileSetName)
        patientHeightsCsvFilePath = self.parameter('patientHeightsCsvFilePath').value()
        patientHeights = None
        if patientHeightsCsvFilePath and patientHeightsCsvFilePath != '':
            patientHeightsDataFrame = pd.read_csv(patientHeightsCsvFilePath)
            patientHeights = self.loadPatientHeights(df=patientHeightsDataFrame)
        outputFileSetName = self.parameter('outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
        outputFileSetPath = self.parameter('outputFileSetPath').value()
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=True)

        files = inputFileSet.files()
        nrSteps = len(files)
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
                fileTuple[0] = file

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
                    outputMetrics[fileTuple[0]]['file'] = fileTuple[0].name()
                    outputMetrics[fileTuple[0]]['muscle_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.MUSCLE, pixelSpacing)
                    if patientHeights:
                        outputMetrics[fileTuple[0]]['muscle_index_pred'] = calculateIndex(
                            area=outputMetrics[fileTuple[0]]['muscle_area_pred'], height=patientHeights[fileTuple[0].name()])
                    outputMetrics[fileTuple[0]]['vat_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.VAT, pixelSpacing)
                    if patientHeights:
                        outputMetrics[fileTuple[0]]['vat_index_pred'] = calculateIndex(
                            area=outputMetrics[fileTuple[0]]['vat_area_pred'], height=patientHeights[fileTuple[0].name()])
                    outputMetrics[fileTuple[0]]['sat_area_pred'] = calculateArea(segmentation, CalculateBodyCompositionMetricsTaskTask.SAT, pixelSpacing)
                    if patientHeights:
                        outputMetrics[fileTuple[0]]['sat_index_pred'] = calculateIndex(
                            area=outputMetrics[fileTuple[0]]['sat_area_pred'], height=patientHeights[fileTuple[0].name()])
                    outputMetrics[fileTuple[0]]['muscle_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.MUSCLE)
                    outputMetrics[fileTuple[0]]['vat_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.VAT)
                    outputMetrics[fileTuple[0]]['sat_ra_pred'] = calculateMeanRadiationAttennuation(image, segmentation, CalculateBodyCompositionMetricsTaskTask.SAT)

                    if tagFile:
                        # Calculate metrics for true segmentation based on TAG file
                        tagImage = self.loadTagFile(file=fileTuple[2], shape=image.shape)
                        outputMetrics[fileTuple[0]]['muscle_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.MUSCLE, pixelSpacing)
                        if patientHeights:
                            outputMetrics[fileTuple[0]]['muscle_index_true'] = calculateIndex(
                                area=outputMetrics[fileTuple[0]]['muscle_area_true'], height=patientHeights[fileTuple[0].name()])
                        outputMetrics[fileTuple[0]]['vat_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.VAT, pixelSpacing)
                        if patientHeights:
                            outputMetrics[fileTuple[0]]['vat_index_true'] = calculateIndex(
                                area=outputMetrics[fileTuple[0]]['vat_area_true'], height=patientHeights[fileTuple[0].name()])
                        outputMetrics[fileTuple[0]]['sat_area_true'] = calculateArea(tagImage, CalculateBodyCompositionMetricsTaskTask.SAT, pixelSpacing)
                        if patientHeights:
                            outputMetrics[fileTuple[0]]['sat_index_true'] = calculateIndex(
                                area=outputMetrics[fileTuple[0]]['sat_area_true'], height=patientHeights[fileTuple[0].name()])
                        outputMetrics[fileTuple[0]]['muscle_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.MUSCLE)
                        outputMetrics[fileTuple[0]]['vat_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.VAT)
                        outputMetrics[fileTuple[0]]['sat_ra_true'] = calculateMeanRadiationAttennuation(image, tagImage, CalculateBodyCompositionMetricsTaskTask.SAT)

                        # Calculate Dice score between segmentation and TAG files
                        outputMetrics[fileTuple[0]]['dice_muscle'] = calculateDiceScore(groundTruth=tagImage, prediction=segmentation, label=CalculateBodyCompositionMetricsTaskTask.MUSCLE)
                        outputMetrics[fileTuple[0]]['dice_vat'] = calculateDiceScore(groundTruth=tagImage, prediction=segmentation, label=CalculateBodyCompositionMetricsTaskTask.VAT)
                        outputMetrics[fileTuple[0]]['dice_sat'] = calculateDiceScore(groundTruth=tagImage, prediction=segmentation, label=CalculateBodyCompositionMetricsTaskTask.SAT)

                    self.addInfo(self.fileOutputMetricsToString(outputMetrics=outputMetrics[fileTuple[0]]))
                else:
                    self.addError(f'Segmentation file {segmentationFile.name()} not found')                        
        
            # Update progress
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
        self.addInfo('Finished')