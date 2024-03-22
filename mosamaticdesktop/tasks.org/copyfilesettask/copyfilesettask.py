import os
import shutil

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class CopyFileSetTask(Task):
    def __init__(self) -> None:
        super(CopyFileSetTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Copies one or more filesets to another fileset'
        )
        self.addMultiFileSetParameter(
            name='inputFileSetNames',
            labelText='Input File Set Names',
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
        inputFileSets = []
        inputFileSetNames = self.parameter('inputFileSetNames').value()
        for inputFileSetName in inputFileSetNames:
            inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
            inputFileSets.append(inputFileSet)
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
        
        # Run task
        step = 0
        nrSteps = 0
        for inputFileSet in inputFileSets:
            nrSteps += len(inputFileSet.files())
        for inputFileSet in inputFileSets:
            for file in inputFileSet.files():

                # Check if the task should cancel
                if self.statusIsCanceled():
                    self.addInfo('Canceling task...')
                    break
                
                shutil.copy(file.path(), outputFileSetPath)

                self.updateProgress(step=step, nrSteps=nrSteps)
                step += 1

        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        self.addInfo('Finished')
