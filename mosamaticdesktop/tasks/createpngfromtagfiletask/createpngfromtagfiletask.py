import os
import numpy as np

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.utils import convertNumPyArrayToPngImage
from mosamaticdesktop.utils import AlbertaColorMap
from mosamaticdesktop.utils import isTagFile, tagPixels
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class CreatePngFromTagFileTask(Task):
    def __init__(self) -> None:
        super(CreatePngFromTagFileTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description=f'Create PNGs From TAG Files',
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set',
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

    def execute(self) -> None:

        # Get parameters needed for this task
        inputFileSetName = self.parameter(name='inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        outputFileSetPath = self.parameter('outputFileSetPath').value()
        outputFileSetName = self.parameter('outputFileSetName').value()
        if outputFileSetName is None:
            outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
        overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=True)

        step = 0
        files = inputFileSet.files()
        nrSteps = len(files)
        for file in files:

            # Check if the task should cancel
            if self.statusIsCanceled():
                self.addInfo('Canceling task...')
                break

            # Create PNGs
            if isTagFile(file.path()):
                numpyArray = tagPixels(tagFilePath=file.path())
                pngImageFileName = os.path.split(file.path())[1] + '.png'
                convertNumPyArrayToPngImage(
                    numpyArrayFilePathOrObject=numpyArray, 
                    colorMap=AlbertaColorMap(),
                    outputDirectoryPath=outputFileSetPath,
                    pngImageFileName=pngImageFileName,
                )

            # Update progress
            self.updateProgress(step=step, nrSteps=nrSteps)
            step += 1
                    
        # Finalize task
        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        self.addInfo('Finished')