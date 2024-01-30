import os
import shutil
import pydicom
import pydicom.errors

from totalsegmentator.python_api import totalsegmentator

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.utils import currentTimeInSeconds, elapsedSeconds
from mosamaticdesktop.logger import Logger

LOGGER = Logger()

ROIS = [
    'vertebrae_S1', 'vertebrae_C1', 'vertebrae_C2', 'vertebrae_C3', 'vertebrae_C4', 'vertebrae_C5', 'vertebrae_C6', 'vertebrae_C7', 
    'vertebrae_L1', 'vertebrae_L2', 'vertebrae_L3', 'vertebrae_L4', 'vertebrae_L5', 'vertebrae_T1', 'vertebrae_T2', 'vertebrae_T3', 
    'vertebrae_T4', 'vertebrae_T5', 'vertebrae_T6', 'vertebrae_T7', 'vertebrae_T8', 'vertebrae_T9', 'vertebrae_T10', 'vertebrae_T11', 
    'vertebrae_T12'
]


class TotalSegmentatorSliceSelectionTask(Task):
    def __init__(self) -> None:
        super(TotalSegmentatorSliceSelectionTask, self).__init__()

    def execute(self) -> None:

        # Get root directory path containing sub-directories for each CT scan
        rootDirectoryPath = self.parameter('rootDirectoryPath').value()
        if rootDirectoryPath:
            outputDirectoryName = self.parameter('outputDirectoryName').value()
            if outputDirectoryName is None:
                outputDirectoryName = self.generateTimestampForFileSetName(name=outputDirectoryName)
            outputDirectoryPath = self.parameter('outputDirectoryPath').value()
            outputDirectoryPath = os.path.join(outputDirectoryPath, outputDirectoryName)
            self.addInfo(f'Output directory path: {outputDirectoryPath}')

            # Check whether to overwrite previous output directory
            overwriteOutputDirectory = self.parameter('overwriteOutputDirectory').value()
            self.addInfo(f'Overwrite output fileset: {overwriteOutputDirectory}')
            if overwriteOutputDirectory:
                if os.path.isdir(outputDirectoryPath):
                    shutil.rmtree(outputDirectoryPath)
            os.makedirs(outputDirectoryPath, exist_ok=True)

            # Get selected vertebra
            vertebra = self.parameter('vertebra').value()
            if vertebra:

                # Each CT scan's files should be in a separate subdirectory inside the root directory
                step = 0
                nrSteps = 0
                for scanDirectoryName in os.listdir(rootDirectoryPath):
                    scanDirectoryPath = os.path.join(rootDirectoryPath, scanDirectoryName)
                    if os.path.isdir(scanDirectoryPath):
                        nrSteps += 1

                for scanDirectoryName in os.listdir(rootDirectoryPath):
                    scanDirectoryPath = os.path.join(rootDirectoryPath, scanDirectoryName)
                    if os.path.isdir(scanDirectoryPath):

                        # Check if task was canceled first
                        if self.statusIsCanceled():
                            self.addInfo('Canceling task...')
                            break

                        # Store all images in dictionary by Z-coordinate
                        zCoords = {}
                        for fileName in os.listdir(scanDirectoryPath):
                            filePath = os.path.join(scanDirectoryPath, fileName)
                            try:
                                p = pydicom.dcmread(filePath, stop_before_pixels=True)
                                if 'ImagePositionPatient' in p:
                                    zCoords[p.ImagePositionPatient[2]] = filePath
                                else:
                                    self.addError(f'ImagePositionPatient attribute not in DICOM image')
                                    break
                            except pydicom.errors.InvalidDicomError:
                                self.addError(f'Image {filePath} of scan {scanDirectoryName} is not valid DICOM')
                                break

                        self.addInfo(f'Running TotalSegmentator on scan directory {scanDirectoryPath}...')
                        outputScanDirectoryPath = os.path.join(outputDirectoryPath, scanDirectoryName)
                        os.makedirs(outputScanDirectoryPath, exist_ok=True)
                        # Run TotalSegmentator to extract all vertebrae. We need this in order to check whether
                        # the vertebra have the correct order and do not overlap
                        start = currentTimeInSeconds()
                        totalsegmentator(
                            scanDirectoryPath, 
                            outputScanDirectoryPath, 
                            fast=True,
                            roi_subset=['liver_vessels'],
                        )
                        self.addInfo(f'Elapsed: {elapsedSeconds(start)} seconds')

                        # Run error checks on extracted vertebrae
                        # https://github.com/MaastrichtU-CDS/2022_EvdWouwer_VertebraSegLabel/blob/main/TS_robustness_check.py

                        # Select wanted vertebra

                        # Do slice selection on vertebra by taking middle slice
                        
                        # Update progress for this iteration         
                        self.updateProgress(step=step, nrSteps=nrSteps)
                        step += 1

                # Build output fileset

                self.addInfo('Finished processing scan directories')
                self.addInfo(f'Results can be found in: {outputDirectoryPath}')
            else:
                self.addError('No vertebra selected')
        else:
            self.addError('No root directory selected')


