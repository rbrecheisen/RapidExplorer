import os
import pydicom
import pydicom.errors
import pandas as pd
import numpy as np

from typing import List

from tasks.task import Task
from data.datamanager import DataManager
from data.file import File
from utils import getPixelsFromDicomObject, tagPixels,
from logger import Logger

LOGGER = Logger()


class CalculateBodyCompositionMetricsTaskTask(Task):
    MUSCLE = 1
    VAT = 5
    SAT = 7

    def __init__(self) -> None:
        super(CalculateBodyCompositionMetricsTaskTask, self).__init__()

    def isDicomFile(file: File) -> bool:
        try:
            pydicom.dcmread(file.path(), stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False

    def findSegmentationFileForDicomFile(self, dicomFile: File, segmentationFile: List[File]) -> str:
        for segmentationFile in segmentationFile.files():
            segmentationFileName = os.path.split(segmentationFile.path())[1]
            if dicomFile + '.seg.npy' == segmentationFileName:
                return segmentationFile
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
                    filePathTuple = [None, None, None]

                    if self.isDicomFile(file=file):
                        filePathTuple[0] = file.path()

                        # Try to find TAG file
                        tagFilePath = self.findTagFilePathForDicomFile(dicomFile=file)
                        if tagFilePath:
                            filePathTuple[2] = tagFilePath

                        # Get segmentation file for DICOM file
                        segmentationFile = self.findSegmentationFileForDicomFile(dicomFile=file, segmentationFiles=inputSegmentationFileSet.files())
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
                

        # Do iterations of the task
        for i in range(nrIterations):
            
            # Check if task was canceled first
            if self.statusIsCanceling():
                canceled = True
                break

            # ==> Do file processing here...

            # Update progress based on nr. steps required. This will automatically
            # send sigals/events to the task widget
            self.updateProgress(step=i, nrSteps=nrIterations)

            # If necessary wait a bit
            time.sleep(1)

        # Terminate task either canceled, error or finished
        if canceled:
            self.setStatusCanceled()
        elif self.hasErrors():
            self.setStatusError()
        else:
            self.setStatusFinished()