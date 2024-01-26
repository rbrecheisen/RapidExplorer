import os
import shutil

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
            if outputFileSetName is None:
                outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
            outputDirectoryPath = self.parameter('outputDirectoryPath').value()
            outputDirectoryPath = os.path.join(outputDirectoryPath, outputDirectoryName)
            self.addInfo(f'Output directory path: {outputDirectoryPath}')

            # Check whether to overwrite previous output directory
            overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
            self.addInfo(f'Overwrite output fileset: {overwriteOutputFileSet}')
            if overwriteOutputFileSet:
                if os.path.isdir(outputDirectoryPath):
                    shutil.rmtree(outputDirectoryPath)
            os.makedirs(outputDirectoryPath, exist_ok=True)

            # Each CT scan's files should be in a separate subdirectory inside the root directory
            for scanDirectoryName in os.listdir(rootDirectoryPath):
                scanDirectoryPath = os.path.join(rootDirectoryPath, scanDirectoryName)
                if os.path.isdir(scanDirectoryPath):
                    self.addInfo(f'Found scan directory: {scanDirectoryPath}')