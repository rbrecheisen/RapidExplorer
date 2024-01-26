import os
import zipfile

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.utils import createNameWithTimestamp
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class CreateArchiveTask(Task):
    def __init__(self) -> None:
        super(CreateArchiveTask, self).__init__()

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

        zipFileName = createNameWithTimestamp(inputFileSet.name()) + '.zip'
        outputZipFilePath = os.path.join(outputFileSetPath, zipFileName)

        step = 0
        files = inputFileSet.files()
        nrSteps = len(files)
        with zipfile.ZipFile(outputZipFilePath, 'w') as zipObj:
            for file in files:
                zipObj.write(file.path(), arcname=os.path.basename(file.path()))

                # Update progress
                self.updateProgress(step=step, nrSteps=nrSteps)
                step += 1

        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        self.addInfo('Finished')
