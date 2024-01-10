import os
import shutil
import pydicom
import pydicom.errors
import pandas as pd
import numpy as np

from typing import List

from tasks.task import Task
from data.datamanager import DataManager
from data.file import File
from utils import getPixelsFromDicomObject, tagPixels, isDicomFile
from logger import Logger

LOGGER = Logger()


class CalculateBodyCompositionMetricsTaskTask(Task):
    MUSCLE = 1
    VAT = 5
    SAT = 7

    def __init__(self) -> None:
        super(CalculateBodyCompositionMetricsTaskTask, self).__init__()

    def findSegmentationFilePathForDicomFile(self, dicomFile: File, segmentationFile: List[File]) -> str:
        for segmentationFile in segmentationFile.files():
            segmentationFilePath = segmentationFile.path()
            segmentationFileName = os.path.split(segmentationFilePath)[1]
            if dicomFile + '.seg.npy' == segmentationFileName:
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

    def run(self) -> None:

        canceled = False
        manager = DataManager()

        # Get input DICOM fileset
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = manager.fileSetByName(name=inputFileSetName)
        if inputFileSet:            
            self.addInfo(f'Input fileset: {inputFileSet.path()}')

            # Get input segmentation fileset
            inputSegmentationFileSetName = self.parameter('inputSegmentationFileSetName').value()
            inputSegmentationFileSet = manager.fileSetByName(inputSegmentationFileSetName)
            if inputSegmentationFileSet:
                self.addInfo(f'Input segmentation fileset: {inputSegmentationFileSet.path()}')

                # Get CSV file with patient heights
                patientHeightsCsvFilePath = self.parameter('patientHeightsCsvFilePath').value()
                if patientHeightsCsvFilePath:
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

                self.addInfo(f'Running task ({self.parameterValuesAsString()})')
                files = inputFileSet.files()
                nrSteps = len(files) + 1
                step = 0
                filePathTuples = []
                for file in files:

                    # Check if task was canceled first
                    if self.statusIsCanceling():
                        canceled = True
                        break

                    filePathTuple = [None, None, None]

                    if isDicomFile(filePath=file.path()):
                        filePathTuple[0] = file.path()

                        # Try to find TAG file
                        tagFilePath = self.findTagFilePathForDicomFile(dicomFile=file)
                        if tagFilePath:
                            filePathTuple[2] = tagFilePath

                        # Get segmentation file for DICOM file
                        segmentationFile = self.findSegmentationFilePathForDicomFile(dicomFile=file, segmentationFiles=inputSegmentationFileSet.files())
                        if segmentationFile:
                            filePathTuple[1] = segmentationFile.path()
                            filePathTuples.append(filePathTuple)

                            # Get DICOM pixels, pixel spacing, predicted segmentation labels and TAG labels if available
                            image, pixelSpacing = self.loadDicomFile(filePath=filePathTuple[0])
                            segmentation = self.loadSegmentationFile(filePath=filePathTuple[1])
                            if tagFilePath:
                                tagImage = self.loadTagFile(filePath=filePathTuple[2])
                                # Build CSV file with predicted and true values
                            else:
                                # Build CSV file with only predicted values
                                pass    
                        else:
                            self.addError(f'Segmentation file {segmentationFile.name()} not found')                        
                
                    # Update progress based on nr. steps required. This will automatically
                    # send sigals/events to the task widget
                    self.updateProgress(step=i, nrSteps=nrSteps)
                    step += 1
                
                # Build output fileset
                self.addInfo(f'Building output fileset: {outputFileSetPath}...')
                manager.createFileSet(fileSetPath=outputFileSetPath)

                # Update final progress
                self.updateProgress(step=step, nrSteps=nrSteps)
                self.addInfo('Finished')                
            else:
                self.addError(f'Segmentation fileset {inputSegmentationFileSetName} not found')
        else:
            self.addError(f'Input fileset {inputFileSetName} not found')

        # Terminate task either canceled, error or finished
        if canceled:
            self.setStatusCanceled()
        elif self.hasErrors():
            self.setStatusError()
        else:
            self.setStatusFinished()