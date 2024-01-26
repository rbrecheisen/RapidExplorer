import os
import shutil

from totalsegmentator.python_api import totalsegmentator

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class TotalSegmentatorTask(Task):
    def __init__(self) -> None:
        super(TotalSegmentatorTask, self).__init__()

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

                    self.addInfo(f'Running TotalSegmentator on scan directory {scanDirectoryPath}...')
                    outputScanDirectoryPath = os.path.join(outputDirectoryPath, scanDirectoryName)
                    os.makedirs(outputScanDirectoryPath, exist_ok=True)
                    totalsegmentator(
                        scanDirectoryPath, outputScanDirectoryPath, fast=True)
                    
                    # Update progress for this iteration         
                    self.updateProgress(step=step, nrSteps=nrSteps)
                    step += 1

            self.addInfo('Finished processing scan directories')
            self.addInfo(f'Results can be found in: {outputDirectoryPath}')