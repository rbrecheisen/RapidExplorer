import os
import shutil

from totalsegmentator.python_api import totalsegmentator

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class TotalSegmentatorRoiSelectionTask(Task):
    def __init__(self) -> None:
        super(TotalSegmentatorRoiSelectionTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Selects identical ROIs from TotalSegmentator outputs'
        )
        self.addPathParameter(
            name='rootDirectoryPath',
            labelText='Root Directory of TotalSegmentator Outputs'
        )
        self.addOptionGroupParameter(
            name='roi',
            labelText='ROI From TotalSegmentator Output',
            options=ROIS,
        )
        self.addPathParameter(
            name='outputFileSetPath',
            labelText='Output File Set Path'
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

    def execute(self) -> None:

        # Get root directory path containing sub-directories for each CT scan
        rootDirectoryPath = self.parameter('rootDirectoryPath').value()
        if rootDirectoryPath:
            roi = self.parameter('roi').value()
            if roi:
                # Setup output fileset path
                outputFileSetName = self.parameter('outputFileSetName').value()
                if outputFileSetName is None:
                    outputFileSetName = self.generateTimestampForFileSetName(name=outputFileSetName)
                outputFileSetPath = self.parameter('outputFileSetPath').value()
                outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
                # Overwrite fileset
                overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
                self.addInfo(f'Overwrite output fileset: {overwriteOutputFileSet}')
                if overwriteOutputFileSet:
                    if os.path.isdir(outputFileSetPath):
                        shutil.rmtree(outputFileSetPath)
                os.makedirs(outputFileSetPath, exist_ok=True)
                self.addInfo(f'Output fileset path: {outputFileSetPath}')

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
                        
                        roiFilePath = os.path.join(scanDirectoryPath, roi + '.nii.gz')
                        roiFileName = scanDirectoryName + '-' + os.path.split(roiFilePath)[1]

                        self.addInfo(f'Copying {roiFilePath} to output fileset...')
                        shutil.copy(roiFilePath, os.path.join(outputFileSetPath, roiFileName))

                        self.updateProgress(step=step, nrSteps=nrSteps)
                        step += 1

                outputFileSet = self.dataManager().createFileSet(fileSetPath=outputFileSetPath)

                self.addInfo('Finished')
            else:
                self.addError('No ROI selected')
        else:
            self.addError('No root directory selected for TotalSegmentator outputs')