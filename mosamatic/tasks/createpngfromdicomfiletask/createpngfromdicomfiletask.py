import os
import numpy as np

from tasks.task import Task
from utils import convertDicomToNumPyArray
from utils import convertNumPyArrayToPngImage
from utils import isDicomFile
from logger import Logger

LOGGER = Logger()


class CreatePngFromDicomFileTask(Task):
    def __init__(self) -> None:
        super(CreatePngFromDicomFileTask, self).__init__()

    def execute(self) -> None:

        # Get parameters needed for this task
        inputFileSetName = self.parameter(name='inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        windowLevel = self.parameter(name='windowLevel').value()
        windowWidth = self.parameter(name='windowWidth').value()
        outputFileSetPath = self.parameter('outputFileSetPath').value()
        outputFileSetName = self.parameter('outputFileSetName').value()
        if outputFileSetName is None:
            outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
        overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=False)

        step = 0
        files = inputFileSet.files()
        nrSteps = len(files)
        for file in files:

            # Check if the task should cancel
            if self.statusIsCanceled():
                self.addInfo('Canceling task...')
                break

            # Create PNGs
            if isDicomFile(file.path()):
                numpyArray = convertDicomToNumPyArray(file.path(), windowLevel=windowLevel, windowWidth=windowWidth)
                pngImageFileName = os.path.split(file.path())[1] + '.png'
                convertNumPyArrayToPngImage(
                    numpyArrayFilePathOrObject=numpyArray, 
                    colorMap=None,
                    outputDirectoryPath=outputFileSetPath,
                    pngImageFileName=pngImageFileName,
                )

            # Update progress
            self.updateProgress(step=step, nrSteps=nrSteps)
            step += 1
                    
        # Finalize task
        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        self.addInfo('Finished')