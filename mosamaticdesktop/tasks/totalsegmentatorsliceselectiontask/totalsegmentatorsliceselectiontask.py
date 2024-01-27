import os
import shutil
import pydicom
import pydicom.errors

from totalsegmentator.python_api import totalsegmentator

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.utils import currentTimeInSeconds, elapsedSeconds
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


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
                        # Running TS will result in separate directories with all the segmentation masks
                        # We can delete all masks that are not the selected one
                        start = currentTimeInSeconds()
                        totalsegmentator(
                            scanDirectoryPath, 
                            outputScanDirectoryPath, 
                            fast=True,
                            roi_subset=[vertebra],
                        )
                        self.addInfo(f'Elapsed: {elapsedSeconds(start)} seconds')

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


